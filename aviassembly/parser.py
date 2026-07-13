"""Parsers for Aviassembly plane-design data."""

from __future__ import annotations

from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from .part import BuildingPart, Decal
from .plane import Plane
from .reader import BinaryReader, GameDataReader
from .types import Vector3


TransformPayloadReader = Callable[[GameDataReader, BuildingPart], None]
MetadataPayloadReader = Callable[[GameDataReader, BuildingPart], None]


@dataclass(slots=True)
class HeaderParser:
    """Parse the header that precedes an Aviassembly plane-data stream.

    ``known_part_names`` mirrors the original game's lookup used to identify
    legacy files, which do not contain an explicit version number.
    """

    known_part_names: Collection[str] = field(default_factory=frozenset)

    def parse(self, reader: GameDataReader) -> Plane:
        """Read a plane header and leave *reader* at the part-data stream."""
        version = self._read_version(reader)
        reader.version = version

        cost = reader.read_float()
        part_count = reader.read_int()
        part_names = [reader.read_string() for _ in range(part_count)]

        return Plane(version=version, cost=cost, part_names=part_names)

    def _read_version(self, reader: GameDataReader) -> int:
        """Use the same legacy-version detection sequence as ``PlaneStorage``."""
        position = reader.get_stream_position()
        reader.read_int()
        reader.read_int()
        first_part_name = reader.read_string()
        reader.set_stream_position(position)

        if first_part_name in self.known_part_names:
            return 18
        return reader.read_int()


@dataclass(slots=True)
class TransformParser:
    """Parse the fixed transform data stored for every plane part.

    The original game writes subtype-specific transform payloads immediately
    after a part's scale. Callers can supply readers for those known part names
    to consume their exact payload before the next part is parsed.
    """

    payload_readers: Mapping[str, TransformPayloadReader] = field(
        default_factory=dict
    )
    track_offsets: bool = False

    def parse(self, reader: GameDataReader) -> list[BuildingPart]:
        """Read the plane-data transform collection from *reader*."""
        part_count = reader.read_int()
        return [self._read_part(reader) for _ in range(part_count)]

    def _read_part(self, reader: GameDataReader) -> BuildingPart:
        name = reader.read_string()
        transform_offset = reader.get_stream_position()
        part = BuildingPart(
            name=name,
            position=reader.read_vector3(),
            rotation=reader.read_quaternion(),
            scale=reader.read_vector3(),
        )

        if self.track_offsets:
            part.extra["_transform_offset"] = transform_offset

        payload_reader = self.payload_readers.get(part.name)
        if payload_reader is not None:
            payload_reader(reader, part)

        return part


@dataclass(slots=True)
class MetadataParser:
    """Parse the ``BuildingPart`` metadata written after part transforms."""

    payload_readers: Mapping[str, MetadataPayloadReader] = field(
        default_factory=dict
    )

    def parse(
        self,
        reader: GameDataReader,
        parts: list[BuildingPart],
    ) -> list[BuildingPart]:
        """Populate metadata for *parts* in the original game save order."""
        for part in parts:
            self._read_part_metadata(reader, part, parts)
        return parts

    def _read_part_metadata(
        self,
        reader: GameDataReader,
        part: BuildingPart,
        parts: Sequence[BuildingPart],
    ) -> None:
        part.has_been_placed = reader.read_bool()
        part.is_base_part = reader.read_bool()

        parent = self._read_part_reference(reader, parts, part)
        if parent is not None:
            self._set_parent(part, parent)

        child_count = reader.read_int()
        for _ in range(child_count):
            child = self._read_part_reference(reader, parts, part)
            if child is None:
                raise ValueError("Unable to resolve a serialized child part reference.")
            self._set_parent(child, part)

        payload_reader = self.payload_readers.get(part.name)
        if payload_reader is not None:
            payload_reader(reader, part)

        if reader.version > 7:
            part.color = reader.read_color()

        if reader.version > 18:
            decal_count = reader.read_int()
            part.decals = [self._read_decal(reader) for _ in range(decal_count)]

    def _read_part_reference(
        self,
        reader: GameDataReader,
        parts: Sequence[BuildingPart],
        ignored_part: BuildingPart,
    ) -> BuildingPart | None:
        if reader.read_bool():
            return None

        position = reader.read_vector3()
        name = reader.read_string()
        best_match: BuildingPart | None = None
        best_distance_squared = float("inf")

        for candidate in parts:
            if candidate is ignored_part or candidate.name != name:
                continue

            distance_squared = self._distance_squared(position, candidate.position)
            if distance_squared < best_distance_squared:
                best_match = candidate
                best_distance_squared = distance_squared

        return best_match

    @staticmethod
    def _set_parent(child: BuildingPart, parent: BuildingPart) -> None:
        if child.parent is not None and child in child.parent.children:
            child.parent.children.remove(child)

        child.parent = parent
        if child not in parent.children:
            parent.children.append(child)

    @staticmethod
    def _distance_squared(first: Vector3, second: Vector3) -> float:
        return (
            (first.x - second.x) ** 2
            + (first.y - second.y) ** 2
            + (first.z - second.z) ** 2
        )

    @staticmethod
    def _read_decal(reader: GameDataReader) -> Decal:
        return Decal(
            name=reader.read_string(),
            color=reader.read_color(),
            layer=reader.read_int(),
            position=reader.read_vector3(),
            rotation=reader.read_quaternion(),
            scale=reader.read_vector3(),
        )


class PlaneParser:
    """Read version-25 plane designs while preserving non-transform payloads."""

    def parse(self, path: str | Path) -> Plane:
        source_path = Path(path)
        source_data = source_path.read_bytes()
        import io

        reader = GameDataReader(BinaryReader(io.BytesIO(source_data)))
        plane = HeaderParser().parse(reader)
        if plane.version != 25:
            raise ValueError(
                "Only current version-25 plane designs can be edited safely; "
                f"received version {plane.version}."
            )

        parts = TransformParser(
            payload_readers={"Body(Clone)": self._read_procedural_fuselage},
            track_offsets=True,
        ).parse(reader)
        plane.parts = parts
        plane.source_data = source_data
        plane.source_path = source_path
        return plane

    @staticmethod
    def _read_procedural_fuselage(
        reader: GameDataReader,
        part: BuildingPart,
    ) -> None:
        """Consume the exact 72-byte ``ProceduralFuselage.Save`` payload."""
        part.extra["procedural_fuselage"] = {
            "side1_radius": reader.read_vector2(),
            "side2_radius": reader.read_vector2(),
            "side1_length_offset": reader.read_vector3(),
            "side2_length_offset": reader.read_vector3(),
            "side1_roundness": reader.read_vector4(),
            "side2_roundness": reader.read_vector4(),
        }
