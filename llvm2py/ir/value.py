from typing import NamedTuple
from .type import Type


class Instruction: ...


class Value(NamedTuple):
    """
    A base class for many IR entities.
    This class can represent a name, a constant, or a constant expression.
    Regardless of the meaning, the value is stored in the val field.

    +-------------------------------------------+-----------------+
    | val kind                                  | val type        |
    +===========================================+=================+
    | Name                                      | str             |
    +-------------------------------------------+-----------------+
    | poison                                    | str("poison")   |
    +-------------------------------------------+-----------------+
    | undef                                     | str("undef)     |
    +-------------------------------------------+-----------------+
    | Integer constant                          | int             |
    +-------------------------------------------+-----------------+
    | Float constant                            | float           |
    +-------------------------------------------+-----------------+
    | Array | Vector of integer constants       | list[int]       |
    +-------------------------------------------+-----------------+
    | Array | Vector of float constants         | list[float]     |
    +-------------------------------------------+-----------------+
    | Null pointer constant                     | None            |
    +-------------------------------------------+-----------------+
    | Array of int8                             | bytes           |
    +-------------------------------------------+-----------------+
    | Block address (Function name, Block name) | tuple[str, str] |
    +-------------------------------------------+-----------------+
    | Constant expression                       | Instruction     |
    +-------------------------------------------+-----------------+

    :param val: Value.
    :type val: str | int | float | list[int] | list[float] | list["Value"] | None | bytes | tuple[str, str] | Instruction)
    :param ty: Value type.
    :type ty: Type
    """

    val: (
        str
        | int
        | float
        | list[int]
        | list[float]
        | list["Value"]
        | None
        | bytes
        | tuple[str, str]
        | Instruction
    )
    ty: Type

    def __str__(self):
        return f"{self.ty} {self.val}"
