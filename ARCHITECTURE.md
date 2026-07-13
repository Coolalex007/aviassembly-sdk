# Architecture

```
aviassembly/

    io/

        binary_reader.py
        binary_writer.py

        game_reader.py
        game_writer.py

    model/

        plane.py
        part.py
        vector.py
        quaternion.py
        color.py

    parser/

        header.py
        transform.py
        metadata.py

    serializer/

    cli/

    blender/

tests/

examples/

docs/
```

BinaryReader

↓

GameDataReader

↓

Parser

↓

Plane Objects

↓

Serializer

↓

Blender

The BinaryReader contains generic binary functionality.

The GameDataReader implements Unity-specific serialization.

Parser classes should never read raw bytes directly.

They only use GameDataReader.

All file parsing should happen in parser/*.
