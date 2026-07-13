from __future__ import annotations

import io
import struct
from dataclasses import dataclass

from .types import Color, Quaternion, Vector3


@dataclass(slots=True)
class GameDataReader:
    reader: io.BufferedReader | io.BytesIO
    version: int = 0

    def read_bool(self) -> bool:
        return struct.unpack("<?", self.reader.read(1))[0]

    def read_int(self) -> int:
        return struct.unpack("<i", self.reader.read(4))[0]

    def read_float(self) -> float:
        return struct.unpack("<f", self.reader.read(4))[0]

    def read_vector3(self) -> Vector3:
        return Vector3(self.read_float(), self.read_float(), self.read_float())

    def read_quaternion(self) -> Quaternion:
        return Quaternion(
            self.read_float(),
            self.read_float(),
            self.read_float(),
            self.read_float(),
        )

    def read_color(self) -> Color:
        return Color(self.read_float(), self.read_float(), self.read_float(), self.read_float())

    def read_string(self) -> str:
        if self.read_bool():
            return ""
        length = self.read_7bit_encoded_int()
        data = self.reader.read(length)
        return data.decode("utf-8", errors="replace")

    def read_7bit_encoded_int(self) -> int:
        result = 0
        shift = 0
        while True:
            byte = self.reader.read(1)
            if not byte:
                raise EOFError("Unexpected end of stream while reading 7-bit encoded int")
            b = byte[0]
            result |= (b & 0x7F) << shift
            if not (b & 0x80):
                return result
            shift += 7
