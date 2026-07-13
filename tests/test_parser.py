from __future__ import annotations

import io

import pytest

from aviassembly import HeaderParser as PublicHeaderParser
from aviassembly import TransformParser as PublicTransformParser
from aviassembly.part import BuildingPart
from aviassembly.parser import HeaderParser, TransformParser
from aviassembly.reader import BinaryReader, GameDataReader
from aviassembly.types import Quaternion, Vector3
from aviassembly.writer import BinaryWriter, GameDataWriter


def test_header_parser_reads_current_plane_header() -> None:
    assert PublicHeaderParser is HeaderParser

    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    writer.write_int(25)
    writer.write_float(1234.5)
    writer.write_int(2)
    writer.write_string("Engine")
    writer.write_string("Wing")
    header_size = writer.get_position()
    writer.write_int(99)

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())))
    plane = HeaderParser().parse(reader)

    assert plane.version == 25
    assert plane.cost == pytest.approx(1234.5)
    assert plane.part_names == ["Engine", "Wing"]
    assert reader.version == 25
    assert reader.get_stream_position() == header_size
    assert reader.read_int() == 99


def test_header_parser_detects_legacy_plane_header_from_known_part() -> None:
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    writer.write_float(500.0)
    writer.write_int(2)
    writer.write_string("Legacy Engine")
    writer.write_string("Wing")

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())))
    plane = HeaderParser(known_part_names={"Legacy Engine"}).parse(reader)

    assert plane.version == 18
    assert plane.cost == pytest.approx(500.0)
    assert plane.part_names == ["Legacy Engine", "Wing"]
    assert reader.version == 18


def test_transform_parser_reads_fixed_part_transforms() -> None:
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    writer.write_int(2)
    writer.write_string("Engine(Clone)")
    writer.write_vector3(Vector3(1.0, 2.0, 3.0))
    writer.write_quaternion(Quaternion(0.0, 0.0, 0.5, 1.0))
    writer.write_vector3(Vector3(1.0, 1.0, 1.0))
    writer.write_string("Wing(Clone)")
    writer.write_vector3(Vector3(-1.0, 0.0, 4.0))
    writer.write_quaternion(Quaternion(0.0, 1.0, 0.0, 0.0))
    writer.write_vector3(Vector3(2.0, 3.0, 4.0))
    transform_end = writer.get_position()
    writer.write_bool(True)

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())))
    parts = TransformParser().parse(reader)

    assert PublicTransformParser is TransformParser
    assert [part.name for part in parts] == ["Engine(Clone)", "Wing(Clone)"]
    assert parts[0].position == Vector3(1.0, 2.0, 3.0)
    assert parts[0].rotation == Quaternion(0.0, 0.0, 0.5, 1.0)
    assert parts[1].scale == Vector3(2.0, 3.0, 4.0)
    assert reader.get_stream_position() == transform_end
    assert reader.read_bool() is True


def test_transform_parser_consumes_registered_subtype_payload() -> None:
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    writer.write_int(1)
    writer.write_string("Custom Part")
    writer.write_vector3(Vector3(0.0, 0.0, 0.0))
    writer.write_quaternion(Quaternion(0.0, 0.0, 0.0, 1.0))
    writer.write_vector3(Vector3(1.0, 1.0, 1.0))
    writer.write_int(42)

    def read_payload(reader: GameDataReader, part: BuildingPart) -> None:
        part.extra["payload"] = reader.read_int()

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())))
    parts = TransformParser(payload_readers={"Custom Part": read_payload}).parse(reader)

    assert parts[0].extra == {"payload": 42}
    assert reader.get_stream().read() == b""
