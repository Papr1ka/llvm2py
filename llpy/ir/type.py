from enum import Enum
from typing import Dict, Any


class TypeID(Enum):
    HalfTyID = 0  # < 16-bit floating point type
    BFloatTyID = 1  # < 16-bit floating point type (7-bit significand)
    FloatTyID = 2  # < 32-bit floating point type
    DoubleTyID = 3  # < 64-bit floating point type
    X86_FP80TyID = 4  # < 80-bit floating point type (X87)
    FP128TyID = 5  # < 128-bit floating point type (112-bit significand)
    PPC_FP128TyID = 6  # < 128-bit floating point type (two 64-bits, PowerPC)
    VoidTyID = 7  # < type with no size
    LabelTyID = 8  # < Labels
    MetadataTyID = 9  # < Metadata
    X86_MMXTyID = 10  # < MMX vectors (64 bits, X86 specific)
    X86_AMXTyID = 11  # < AMX vectors (8192 bits, X86 specific)
    TokenTyID = 12  # < Tokens

    # Derived types
    IntegerTyID = 13  # < Arbitrary bit width integers
    FunctionTyID = 14  # < Functions
    PointerTyID = 15  # < Pointers
    StructTyID = 16  # < Structures
    ArrayTyID = 17  # < Arrays
    FixedVectorTyID = 18  # < Fixed width SIMD vector type
    ScalableVectorTyID = 19  # < Scalable SIMD vector type
    TypedPointerTyID = 20  # < Typed pointer used by some GPU targets
    TargetExtTyID = 21


class Type:
    name: str
    type_id: TypeID

    # Not None if Type is type_id is ArrayTyID
    num_elements: int
    subtype: "Type"

    _fields = (
        'name',
        'type_id',
        'array'
    )

    def __init__(self, name: str, type_id: int, data: Dict[str, Any]):
        self.name = name
        self.type_id = TypeID(type_id)
        self.num_elements = data.get("num_elements")
        self.subtype = data.get("subtype")

    def __repr__(self):
        return f"<Type name={self.name}, type_id={self.type_id}>"
