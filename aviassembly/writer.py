"""Generic little-endian binary writing helpers."""

from __future__ import annotations

import io
import struct
from dataclasses import dataclass
from typing import BinaryIO, Iterable

from .types import Color, Quaternion, Vector2, Vector3, Vector4


@dataclass(slots=True)
class BinaryWriter:
    """Write primitive values to a writable binary stream.

    The class mirrors :class:`aviassembly.reader.BinaryReader` and contains no
    Aviassembly-specific serialization rules.
    """

    stream: BinaryIO

    def __post_init__(self) -> None:
        if not self.stream.writable():
            raise ValueError("Stream must be writable.")

    @property
    def position(self) -> int:
        """Return the current stream position."""
        return self.stream.tell()

    @property
    def length(self) -> int:
        """Return the stream length without changing its current position."""
        position = self.position
        self.stream.seek(0, io.SEEK_END)
        length = self.position
        self.stream.seek(position)
        return length

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> None:
        """Set the stream position."""
        self.stream.seek(offset, whence)

    def skip(self, count: int) -> None:
        """Move the current position by *count* bytes."""
        self.seek(count, io.SEEK_CUR)

    def write(self, data: bytes) -> None:
        """Write raw bytes, raising if the stream performs a short write."""
        bytes_written = self.stream.write(data)
        if bytes_written != len(data):
            raise OSError(
                f"Expected to write {len(data)} bytes but wrote {bytes_written}."
            )

    def bool(self, value: bool) -> None:
        self.write(struct.pack("<?", value))

    def int8(self, value: int) -> None:
        self.write(struct.pack("<b", value))

    def uint8(self, value: int) -> None:
        self.write(struct.pack("<B", value))

    def int16(self, value: int) -> None:
        self.write(struct.pack("<h", value))

    def uint16(self, value: int) -> None:
        self.write(struct.pack("<H", value))

    def int32(self, value: int) -> None:
        self.write(struct.pack("<i", value))

    def uint32(self, value: int) -> None:
        self.write(struct.pack("<I", value))

    def int64(self, value: int) -> None:
        self.write(struct.pack("<q", value))

    def uint64(self, value: int) -> None:
        self.write(struct.pack("<Q", value))

    def float(self, value: float) -> None:
        self.write(struct.pack("<f", value))

    def double(self, value: float) -> None:
        self.write(struct.pack("<d", value))

    def bytes(self, value: bytes) -> None:
        """Write a byte sequence without a length prefix."""
        self.write(value)

    def float_array(self, values: Iterable[float]) -> None:
        for value in values:
            self.float(value)

    def int32_array(self, values: Iterable[int]) -> None:
        for value in values:
            self.int32(value)

    def string(self, value: str) -> None:
        """Write a .NET ``BinaryWriter`` UTF-8 string."""
        encoded = value.encode("utf-8")
        self.write_7bit_encoded_int(len(encoded))
        self.write(encoded)

    def write_7bit_encoded_int(self, value: int) -> None:
        """Write a non-negative integer using .NET's 7-bit encoding."""
        if value < 0:
            raise ValueError("7-bit encoded integers must be non-negative.")

        while value >= 0x80:
            self.uint8((value & 0x7F) | 0x80)
            value >>= 7
        self.uint8(value)

    def align(self, alignment: int, fill_byte: int = 0) -> None:
        """Pad with *fill_byte* until the position is a multiple of *alignment*."""
        if alignment <= 0:
            raise ValueError("Alignment must be positive.")
        if not 0 <= fill_byte <= 0xFF:
            raise ValueError("Fill byte must be between 0 and 255.")

        padding = (-self.position) % alignment
        if padding:
            self.write(bytes([fill_byte]) * padding)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(position={self.position}, length={self.length})"


@dataclass(slots=True)
class GameDataWriter:
    """Write the Unity value encodings used by Aviassembly game data."""

    writer: BinaryWriter

    def write(self, value: object) -> None:
        """Write a value supported by the C# ``GameDataWriter`` overloads.

        Python has one ``int`` and one ``float`` type, so 64-bit integers and
        doubles are intentionally written through :meth:`write_long` and
        :meth:`write_double` rather than inferred from a value.
        """
        if value is None or isinstance(value, str):
            self.write_string(value)
        elif isinstance(value, bool):
            self.write_bool(value)
        elif isinstance(value, int):
            self.write_int(value)
        elif isinstance(value, float):
            self.write_float(value)
        elif isinstance(value, Quaternion):
            self.write_quaternion(value)
        elif isinstance(value, Vector2):
            self.write_vector2(value)
        elif isinstance(value, Vector3):
            self.write_vector3(value)
        elif isinstance(value, Vector4):
            self.write_vector4(value)
        elif isinstance(value, Color):
            self.write_color(value)
        else:
            raise TypeError(f"Unsupported GameData value: {type(value).__name__}.")

    def write_bool(self, value: bool) -> None:
        self.writer.bool(value)

    def write_string(self, value: str | None) -> None:
        """Write a C# ``string.IsNullOrEmpty`` sentinel and its value."""
        is_null_or_empty = not value
        self.writer.bool(is_null_or_empty)
        if not is_null_or_empty:
            self.writer.string(value)

    def write_float(self, value: float) -> None:
        self.writer.float(value)

    def write_double(self, value: float) -> None:
        self.writer.double(value)

    def write_int(self, value: int) -> None:
        self.writer.int32(value)

    def write_long(self, value: int) -> None:
        self.writer.int64(value)

    def write_quaternion(self, value: Quaternion) -> None:
        self.writer.float(value.x)
        self.writer.float(value.y)
        self.writer.float(value.z)
        self.writer.float(value.w)

    def write_vector2(self, value: Vector2) -> None:
        self.writer.float(value.x)
        self.writer.float(value.y)

    def write_vector3(self, value: Vector3) -> None:
        self.writer.float(value.x)
        self.writer.float(value.y)
        self.writer.float(value.z)

    def write_vector4(self, value: Vector4) -> None:
        self.writer.float(value.x)
        self.writer.float(value.y)
        self.writer.float(value.z)
        self.writer.float(value.w)

    def write_color(self, value: Color) -> None:
        self.writer.float(value.r)
        self.writer.float(value.g)
        self.writer.float(value.b)
        self.writer.float(value.a)

    def write_type_name(self, value: str) -> None:
        """Write a raw C# assembly-qualified type name without a sentinel."""
        self.writer.string(value)

    def write_type(self, value: str) -> None:
        """Compatibility alias for :meth:`write_type_name`."""
        self.write_type_name(value)

    def get_position(self) -> int:
        return self.writer.position

    def write_stream(self, stream: BinaryIO) -> None:
        """Copy *stream* from its start, matching C# ``Stream.CopyTo`` usage."""
        stream.seek(0)
        while data := stream.read(1024 * 1024):
            self.writer.write(data)
