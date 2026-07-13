"""Parsers for Aviassembly plane-design data."""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass, field

from .plane import Plane
from .reader import GameDataReader


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


class PlaneParser:
    def parse(self, path: str) -> Plane:
        raise NotImplementedError("Parser implementation in progress.")
