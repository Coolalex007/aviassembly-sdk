from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .types import Color, Quaternion, Vector3


@dataclass(slots=True)
class Decal:
    name: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    color: Color | None = None
    layer: int = 0
    position: Vector3 = field(default_factory=lambda: Vector3(0.0, 0.0, 0.0))
    rotation: Quaternion = field(
        default_factory=lambda: Quaternion(0.0, 0.0, 0.0, 1.0)
    )
    scale: Vector3 = field(default_factory=lambda: Vector3(1.0, 1.0, 1.0))


@dataclass(slots=True)
class BuildingPart:
    name: str
    position: Vector3
    rotation: Quaternion
    scale: Vector3
    has_been_placed: bool = False
    is_base_part: bool = False
    parent: "BuildingPart | None" = None
    children: list["BuildingPart"] = field(default_factory=list)
    color: Color | None = None
    decals: list[Decal] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)
