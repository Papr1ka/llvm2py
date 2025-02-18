from typing import NamedTuple
from .type import Type


class Instruction: ...


class Value(NamedTuple):
    """
    A base class for many IR entities

    A class can represent a name, a constant, or a constant expression

    Regardless of the meaning, the value is stored in the val field

    Constant aggregate zero (zeroinitializer) represented by int(0)
    """

    # fmt: off
    val: (
        str                         # Name
        | int                       # Constant int (not int8)
        | float                     # Constant float
        | list[int]                 # Constant Data {Array | Vector} of integers
        | list[float]               # Constant Data {Array | Vector} of FP values
        | list["Value"]             # Constant Aggregates (Array | Vector | Struct) of Values 
        | None                      # Constant Null Pointer
        | bytes                     # Array of int8 (CString for example)
        | tuple[str, str]           # Block address (Function name, Block name)
        | Instruction               # Constant expression
    )
    # fmt: on
    ty: Type  # Value type

    def __str__(self):
        return f"{self.ty} {self.val}"
