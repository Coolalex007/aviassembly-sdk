from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Vector3:
    x: float
    y: float
    z: float


@dataclass(slots=True)
class Quaternion:
    x: float
    y: float
    z: float
    w: float


@dataclass(slots=True)
class Color:
    r: float
    g: float
    b: float
    a: float
