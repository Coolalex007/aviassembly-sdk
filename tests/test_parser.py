from __future__ import annotations

import io

import pytest

from aviassembly import HeaderParser as PublicHeaderParser
from aviassembly import MetadataParser as PublicMetadataParser
from aviassembly import TransformParser as PublicTransformParser
from aviassembly.part import BuildingPart, Decal
from aviassembly.parser import HeaderParser, MetadataParser, TransformParser
from aviassembly.reader import BinaryReader, GameDataReader
from aviassembly.types import Color, Quaternion, Vector3
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


def test_metadata_parser_reads_relationships_colors_and_decals() -> None:
    root = BuildingPart(
        name="Root",
        position=Vector3(0.0, 0.0, 0.0),
        rotation=Quaternion(0.0, 0.0, 0.0, 1.0),
        scale=Vector3(1.0, 1.0, 1.0),
    )
    engine = BuildingPart(
        name="Engine",
        position=Vector3(4.0, 5.0, 6.0),
        rotation=Quaternion(0.0, 0.0, 0.0, 1.0),
        scale=Vector3(1.0, 1.0, 1.0),
    )
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))

    _write_metadata_prefix(writer, has_been_placed=False, is_base_part=True, parent=None)
    writer.write_int(1)
    _write_part_reference(writer, engine)
    writer.write_color(Color(0.1, 0.2, 0.3, 0.4))
    writer.write_int(1)
    writer.write_string("Roundel")
    writer.write_color(Color(0.5, 0.6, 0.7, 0.8))
    writer.write_int(3)
    writer.write_vector3(Vector3(1.0, 2.0, 3.0))
    writer.write_quaternion(Quaternion(0.0, 0.0, 0.0, 1.0))
    writer.write_vector3(Vector3(2.0, 2.0, 2.0))

    _write_metadata_prefix(
        writer,
        has_been_placed=True,
        is_base_part=False,
        parent=root,
    )
    writer.write_int(0)
    writer.write_color(Color(0.9, 0.8, 0.7, 0.6))
    writer.write_int(0)

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())), version=25)
    parts = MetadataParser().parse(reader, [root, engine])

    assert PublicMetadataParser is MetadataParser
    assert parts == [root, engine]
    assert root.has_been_placed is False
    assert root.is_base_part is True
    assert engine.parent is root
    assert root.children == [engine]
    assert _color_values(root.color) == pytest.approx((0.1, 0.2, 0.3, 0.4))
    assert _color_values(engine.color) == pytest.approx((0.9, 0.8, 0.7, 0.6))
    assert len(root.decals) == 1
    assert root.decals[0].name == "Roundel"
    assert root.decals[0].layer == 3
    assert root.decals[0].position == Vector3(1.0, 2.0, 3.0)
    assert _color_values(root.decals[0].color) == pytest.approx((0.5, 0.6, 0.7, 0.8))
    assert reader.get_stream().read() == b""


def test_metadata_parser_consumes_registered_plane_part_payload() -> None:
    part = BuildingPart(
        name="Custom Part",
        position=Vector3(0.0, 0.0, 0.0),
        rotation=Quaternion(0.0, 0.0, 0.0, 1.0),
        scale=Vector3(1.0, 1.0, 1.0),
    )
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    _write_metadata_prefix(writer, has_been_placed=True, is_base_part=False, parent=None)
    writer.write_int(0)
    writer.write_int(42)
    writer.write_color(Color(1.0, 1.0, 1.0, 1.0))
    writer.write_int(0)

    def read_payload(reader: GameDataReader, parsed_part: BuildingPart) -> None:
        parsed_part.extra["payload"] = reader.read_int()

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())), version=25)
    parts = MetadataParser(payload_readers={"Custom Part": read_payload}).parse(
        reader, [part]
    )

    assert parts[0].extra == {"payload": 42}
    assert _color_values(parts[0].color) == (1.0, 1.0, 1.0, 1.0)
    assert reader.get_stream().read() == b""


def test_metadata_parser_honors_color_and_decal_version_gates() -> None:
    part = BuildingPart(
        name="Legacy Part",
        position=Vector3(0.0, 0.0, 0.0),
        rotation=Quaternion(0.0, 0.0, 0.0, 1.0),
        scale=Vector3(1.0, 1.0, 1.0),
    )
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    _write_metadata_prefix(writer, has_been_placed=False, is_base_part=False, parent=None)
    writer.write_int(0)
    writer.write_bool(True)

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())), version=7)
    MetadataParser().parse(reader, [part])

    assert part.color is None
    assert part.decals == []
    assert reader.read_bool() is True


def test_metadata_parser_selects_the_nearest_matching_part_reference() -> None:
    first_wing = BuildingPart(
        name="Wing",
        position=Vector3(0.0, 0.0, 0.0),
        rotation=Quaternion(0.0, 0.0, 0.0, 1.0),
        scale=Vector3(1.0, 1.0, 1.0),
    )
    second_wing = BuildingPart(
        name="Wing",
        position=Vector3(10.0, 0.0, 0.0),
        rotation=Quaternion(0.0, 0.0, 0.0, 1.0),
        scale=Vector3(1.0, 1.0, 1.0),
    )
    source_part = BuildingPart(
        name="Engine",
        position=Vector3(5.0, 0.0, 0.0),
        rotation=Quaternion(0.0, 0.0, 0.0, 1.0),
        scale=Vector3(1.0, 1.0, 1.0),
    )
    stream = io.BytesIO()
    writer = GameDataWriter(BinaryWriter(stream))
    writer.write_bool(False)
    writer.write_vector3(Vector3(9.0, 0.0, 0.0))
    writer.write_string("Wing")

    reader = GameDataReader(BinaryReader(io.BytesIO(stream.getvalue())))
    resolved = MetadataParser()._read_part_reference(
        reader, [first_wing, second_wing, source_part], source_part
    )

    assert resolved is second_wing


def test_decal_preserves_its_existing_positional_data_argument() -> None:
    decal = Decal("Legacy Decal", {"source": "existing caller"})

    assert decal.name == "Legacy Decal"
    assert decal.data == {"source": "existing caller"}


def _write_metadata_prefix(
    writer: GameDataWriter,
    *,
    has_been_placed: bool,
    is_base_part: bool,
    parent: BuildingPart | None,
) -> None:
    writer.write_bool(has_been_placed)
    writer.write_bool(is_base_part)
    _write_part_reference(writer, parent)


def _write_part_reference(writer: GameDataWriter, part: BuildingPart | None) -> None:
    writer.write_bool(part is None)
    if part is not None:
        writer.write_vector3(part.position)
        writer.write_string(part.name)


def _color_values(color: Color | None) -> tuple[float, float, float, float]:
    assert color is not None
    return color.r, color.g, color.b, color.a
