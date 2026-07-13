from __future__ import annotations

import io
import struct
from dataclasses import dataclass

from .types import Color, Quaternion, Vector3


@dataclass(slots=True)
class GameDataWriter:
    writer: io.BufferedWriter | io.BytesIO

    def write_bool(self, value: bool) -> None:
        self.writer.write(struct.pack("<?", value))

    def write_int(self, value: int) -> None:
        self.writer.write(struct.pack("<i", value))

    def write_float(self, value: float) -> None:
        self.writer.write(struct.pack("<f", value))

    def write_vector3(self, value: Vector3) -> None:
        self.write_float(value.x)
        self.write_float(value.y)
        self.write_float(value.z)

    def write_quaternion(self, value: Quaternion) -> None:
        self.write_float(value.x)
        self.write_float(value.y)
        self.write_float(value.z)
        self.write_float(value.w)

    def write_color(self, value: Color) -> None:
        self.write_float(value.r)
        self.write_float(value.g)
        self.write_float(value.b)
        self.write_float(value.a)

    def write_string(self, value: str) -> None:
        if value == "":
            self.write_bool(True)
            return
        self.write_bool(False)
        data = value.encode("utf-8")
        self.write_7bit_encoded_int(len(data))
        self.writer.write(data)

    def write_7bit_encoded_int(self, value: int) -> None:
        n = value
        while n >= 0x80:
            self.writer.write(bytes([(n & 0x7F) | 0x80]))
            n >>= 7
        self.writer.write(bytes([n]))
