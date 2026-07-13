# aviassembly-sdk

Python tooling for reading, inspecting, and eventually importing/exporting Aviassembly `.planedesign` files.

## Current status

- Reverse engineering the file format
- Building a parser for the save structure
- Planning a Blender importer/exporter

## Planned layout

- `aviassembly/` – core Python package
- `blender_addon/` – Blender integration
- `docs/` – file format notes
- `tests/` – parser tests

## Notes

This project is being built from the game's own save/load code so the parser can match the original format as closely as possible.
