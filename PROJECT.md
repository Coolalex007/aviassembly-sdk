# Aviassembly SDK

## Goal

Create a complete open-source SDK for Aviassembly.

The SDK should be able to

- read .planedesign files
- write .planedesign files
- validate files
- export/import JSON
- provide a Blender addon
- later support mesh importing from Unity assets

This project is **NOT** intended for cheating or bypassing DRM.

It only exists to allow users to edit their own aircraft outside the game.

---

# Philosophy

This project should be developed like a professional open source library.

Requirements:

- Clean architecture
- Type hints
- Dataclasses
- Unit tests
- Documentation
- Small commits
- No quick hacks
- Python 3.11+

Every feature should be tested before merging.

---

# Development Workflow

Each milestone should result in working code.

Current roadmap:

v0.1.1

- BinaryReader
- BinaryWriter
- GameDataReader
- GameDataWriter

v0.1.2

- Header Parser

v0.1.3

- Transform Parser

v0.1.4

- BuildingPart Metadata

v0.2.0

- JSON Export

v0.3.0

- Blender Import

v1.0.0

- Complete Import/Export