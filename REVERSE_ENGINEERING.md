# Reverse Engineering

## SaveToFile()

The file starts with

Version

Plane Cost

Part Count

Part Names

Memory Stream

---

Version

```
Write(25)
```

Current version is

25

---

Header

```
Version

Cost

PartCount

PartNames

```

After the header follows a MemoryStream.

---

Memory Stream

PlaneStorage.Save()

writes

```
PartCount

Transform for every part

Metadata for every part
```

---

Transform

Each part stores

```
Name

Position

Rotation

Scale
```

Position

Vector3

Rotation

Quaternion

Scale

Vector3

---

Metadata

BuildingPart.Save()

stores

```
hasBeenPlaced

isBasePart

Parent

Children

PlanePart.Save()

Color

Decals
```

---

SaveBuildingPart()

stores

```
bool isNull

if not null

Position

Part Name
```

Parent references are not stored using IDs.

Instead they are stored by

Position

+

Part Name

---

PlanePart

PlanePart itself stores nothing.

```
virtual Save()

virtual Load()
```

are empty.

Only subclasses override Save().

---

Known subclasses

Engine

Rotator

Decoupler

Most aircraft parts do not override Save().

---

Known serialization

Vector3

```
float

float

float
```

Quaternion

```
float

float

float

float
```

String

```
bool

BinaryReader.ReadString()
```

Empty strings are stored as

```
true
```

otherwise

```
false

7-bit encoded string length

utf8 bytes
```

---

Known Save Order

```
Header

↓

MemoryStream

↓

Transforms

↓

Metadata

↓

Special Part Data

↓

Color

↓

Decals
```
