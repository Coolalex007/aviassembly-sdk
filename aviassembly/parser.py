from __future__ import annotations

from pathlib import Path

from .plane import Plane
from .reader import GameDataReader


class PlaneParser:
    def parse(self, path: str | Path) -> Plane:
        file_path = Path(path)
        with file_path.open("rb") as f:
            reader = GameDataReader(f)
            version = reader.read_int()
            cost = reader.read_float()
            part_count = reader.read_int()
            part_names = [reader.read_string() for _ in range(part_count)]
            # The remaining payload is the serialized plane stream.
            # We keep the raw stream handling for the next iteration once
            # the exact nested structure is fully mapped.
            return Plane(version=version, cost=cost, part_names=part_names, parts=[])
