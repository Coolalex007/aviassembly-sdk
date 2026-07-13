"""Lossless transform export for current Aviassembly plane designs."""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path

from .part import BuildingPart
from .plane import Plane


@dataclass(slots=True)
class PlaneWriter:
    """Write edited transforms into a plane design's original byte stream.

    Component-specific settings are not inferable from extracted meshes. This
    writer retains every byte outside transform records, preserving them.
    """

    def write(self, plane: Plane, path: str | Path) -> Path:
        if plane.version != 25:
            raise ValueError("Only version-25 plane designs can be exported.")
        if plane.source_data is None:
            raise ValueError("Plane has no source data to preserve.")

        data = bytearray(plane.source_data)
        for part in plane.parts:
            offset = part.extra.get("_transform_offset")
            if not isinstance(offset, int):
                raise ValueError("Each exported part must originate from PlaneParser.")
            self._write_transform(data, offset, part)

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(data)
        return output_path

    @staticmethod
    def _write_transform(data: bytearray, offset: int, part: BuildingPart) -> None:
        struct.pack_into(
            "<10f",
            data,
            offset,
            part.position.x,
            part.position.y,
            part.position.z,
            part.rotation.x,
            part.rotation.y,
            part.rotation.z,
            part.rotation.w,
            part.scale.x,
            part.scale.y,
            part.scale.z,
        )
