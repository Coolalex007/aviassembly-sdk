"""
aviassembly.io.binary_reader

Generic little-endian binary reader used by the Aviassembly SDK.

This class intentionally contains no Aviassembly-specific logic.
Unity/GameData serialization is implemented in GameDataReader.
"""

from __future__ import annotations

import io
import struct


class BinaryReader:
    """Generic binary reader."""

    def __init__(self, stream: io.BufferedIOBase):
        if not stream.readable():
            raise ValueError("Stream must be readable.")

        self.stream = stream

    # --------------------------------------------------------
    # Position
    # --------------------------------------------------------

    @property
    def position(self) -> int:
        return self.stream.tell()

    @property
    def length(self) -> int:
        pos = self.stream.tell()
        self.stream.seek(0, io.SEEK_END)
        length = self.stream.tell()
        self.stream.seek(pos)
        return length

    @property
    def remaining(self) -> int:
        return self.length - self.position

    def seek(self, offset: int, whence: int = io.SEEK_SET):
        self.stream.seek(offset, whence)

    def skip(self, count: int):
        self.seek(count, io.SEEK_CUR)

    # --------------------------------------------------------
    # Raw
    # --------------------------------------------------------

    def read(self, count: int) -> bytes:
        data = self.stream.read(count)

        if len(data) != count:
            raise EOFError(
                f"Expected {count} bytes "
                f"but received {len(data)}."
            )

        return data

    def peek(self, count: int) -> bytes:
        pos = self.position
        data = self.read(count)
        self.seek(pos)
        return data

    # --------------------------------------------------------
    # Primitive Types
    # --------------------------------------------------------

    def bool(self) -> bool:
        return struct.unpack("<?", self.read(1))[0]

    def int8(self) -> int:
        return struct.unpack("<b", self.read(1))[0]

    def uint8(self) -> int:
        return struct.unpack("<B", self.read(1))[0]

    def int16(self) -> int:
        return struct.unpack("<h", self.read(2))[0]

    def uint16(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def int32(self) -> int:
        return struct.unpack("<i", self.read(4))[0]

    def uint32(self) -> int:
        return struct.unpack("<I", self.read(4))[0]

    def int64(self) -> int:
        return struct.unpack("<q", self.read(8))[0]

    def uint64(self) -> int:
        return struct.unpack("<Q", self.read(8))[0]

    def float(self) -> float:
        return struct.unpack("<f", self.read(4))[0]

    def double(self) -> float:
        return struct.unpack("<d", self.read(8))[0]

    # --------------------------------------------------------
    # Arrays
    # --------------------------------------------------------

    def bytes(self, length: int) -> bytes:
        return self.read(length)

    def float_array(self, count: int):
        return [self.float() for _ in range(count)]

    def int32_array(self, count: int):
        return [self.int32() for _ in range(count)]

    # --------------------------------------------------------
    # Utility
    # --------------------------------------------------------

    def align(self, alignment: int):
        """
        Aligns the stream position.

        Example:
            align(4)
        """

        remainder = self.position % alignment

        if remainder:
            self.skip(alignment - remainder)

    def eof(self) -> bool:
        return self.remaining == 0

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(position={self.position}, "
            f"remaining={self.remaining})"
        )