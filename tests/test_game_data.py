from __future__ import annotations

import io

import pytest

from aviassembly.reader import BinaryReader, GameDataReader
from aviassembly.types import Color, Quaternion, Vector2, Vector3, Vector4
from aviassembly.writer import BinaryWriter, GameDataWriter


def test_game_data_string_encoding_matches_csharp_writer() -> None:
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))

    writer.write_string(None)
    writer.write_string("")
    writer.write_string("A")
    writer.write_type_name("Engine, Assembly-CSharp")

    assert stream.getvalue() == (
        b"\x01\x01\x00\x01A\x17Engine, Assembly-CSharp"
    )


def test_game_data_round_trips_supported_values() -> None:
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    writer.write(True)
    writer.write(42)
    writer.write(1.5)
    writer.write_double(2.5)
    writer.write_long(2**40)
    writer.write("part")
    writer.write(Quaternion(1.0, 2.0, 3.0, 4.0))
    writer.write(Vector2(5.0, 6.0))
    writer.write(Vector3(7.0, 8.0, 9.0))
    writer.write(Vector4(10.0, 11.0, 12.0, 13.0))
    writer.write(Color(0.1, 0.2, 0.3, 0.4))
    writer.write_type("Engine, Assembly-CSharp")

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())), version=25)

    assert reader.version == 25
    assert reader.read_bool() is True
    assert reader.read_int() == 42
    assert reader.read_float() == pytest.approx(1.5)
    assert reader.read_double() == pytest.approx(2.5)
    assert reader.read_long() == 2**40
    assert reader.read_string() == "part"
    assert reader.read_quaternion() == Quaternion(1.0, 2.0, 3.0, 4.0)
    assert reader.read_vector2() == Vector2(5.0, 6.0)
    assert reader.read_vector3() == Vector3(7.0, 8.0, 9.0)
    assert reader.read_vector4() == Vector4(10.0, 11.0, 12.0, 13.0)
    color = reader.read_color()
    assert (color.r, color.g, color.b, color.a) == pytest.approx((0.1, 0.2, 0.3, 0.4))
    assert reader.read_type() == "Engine, Assembly-CSharp"


def test_game_data_stream_copy_and_position_helpers() -> None:
    destination = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(destination))
    source = io.BytesIO(b"stream-data")
    source.seek(4)

    writer.write_stream(source)

    reader = GameDataReader(BinaryReader(io.BytesIO(destination.getvalue())))
    assert writer.get_position() == len(b"stream-data")
    assert destination.getvalue() == b"stream-data"
    assert source.tell() == len(b"stream-data")
    assert reader.get_stream_position() == 0
    reader.set_stream_position(6)
    assert reader.get_stream().read() == b"-data"


def test_game_data_rejects_invalid_7bit_string_lengths() -> None:
    reader = GameDataReader(BinaryReader(io.BytesIO(b"\x00\x80\x80\x80\x80\x80")))

    with pytest.raises(ValueError, match="Invalid 7-bit"):
        reader.read_string()
