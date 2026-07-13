from __future__ import annotations

import io
import struct

import pytest

from aviassembly.writer import BinaryWriter


def test_writes_little_endian_primitives() -> None:
    stream = io.BytesIO()
    writer = BinaryWriter(stream)

    writer.bool(True)
    writer.int8(-1)
    writer.uint8(255)
    writer.int16(-2)
    writer.uint16(65535)
    writer.int32(-3)
    writer.uint32(2**32 - 1)
    writer.int64(-4)
    writer.uint64(2**64 - 1)
    writer.float(1.5)
    writer.double(2.5)

    assert stream.getvalue() == struct.pack(
        "<?bBhHiIqQfd",
        True,
        -1,
        255,
        -2,
        65535,
        -3,
        2**32 - 1,
        -4,
        2**64 - 1,
        1.5,
        2.5,
    )


def test_writes_dotnet_compatible_utf8_strings() -> None:
    stream = io.BytesIO()
    writer = BinaryWriter(stream)

    writer.string("€")
    writer.string("a" * 128)

    assert stream.getvalue() == b"\x03\xe2\x82\xac\x80\x01" + b"a" * 128


def test_writes_arrays_and_aligns_position() -> None:
    stream = io.BytesIO()
    writer = BinaryWriter(stream)

    writer.bytes(b"A")
    writer.align(4, fill_byte=255)
    writer.float_array([1.0, 2.0])
    writer.int32_array([3, 4])

    assert writer.position == writer.length == 20
    assert stream.getvalue() == (
        b"A\xff\xff\xff"
        + struct.pack("<ffii", 1.0, 2.0, 3, 4)
    )


def test_rejects_invalid_7bit_values_and_alignment() -> None:
    writer = BinaryWriter(io.BytesIO())

    with pytest.raises(ValueError, match="non-negative"):
        writer.write_7bit_encoded_int(-1)

    with pytest.raises(ValueError, match="positive"):
        writer.align(0)
