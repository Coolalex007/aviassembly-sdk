from __future__ import annotations

import io

import pytest

from aviassembly import HeaderParser as PublicHeaderParser
from aviassembly.parser import HeaderParser
from aviassembly.reader import BinaryReader, GameDataReader
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
