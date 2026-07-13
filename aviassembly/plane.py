from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .part import BuildingPart


@dataclass(slots=True)
class Plane:
    version: int
    cost: float
    part_names: list[str] = field(default_factory=list)
    parts: list[BuildingPart] = field(default_factory=list)
    source_data: bytes | None = None
    source_path: Path | None = None
