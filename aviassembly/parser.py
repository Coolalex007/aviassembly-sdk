"""Parsers for Aviassembly plane-design data."""

from __future__ import annotations

from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field

from .part import BuildingPart
from .plane import Plane
from .reader import GameDataReader


TransformPayloadReader = Callable[[GameDataReader, BuildingPart], None]


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

    def parse(self, reader: GameDataReader) -> list[BuildingPart]:
        """Read the plane-data transform collection from *reader*."""
        part_count = reader.read_int()
        return [self._read_part(reader) for _ in range(part_count)]

    def _read_part(self, reader: GameDataReader) -> BuildingPart:
        part = BuildingPart(
            name=reader.read_string(),
            position=reader.read_vector3(),
            rotation=reader.read_quaternion(),
            scale=reader.read_vector3(),
        )

        payload_reader = self.payload_readers.get(part.name)
        if payload_reader is not None:
            payload_reader(reader, part)

        return part


class PlaneParser:
    def parse(self, path: str) -> Plane:
        raise NotImplementedError("Parser implementation in progress.")
