from dataclasses import dataclass

from .support import attrs_to_dict

from .global_object import GlobalObject

from .block import Block
from .value import Value
from .instruction import Attrs
from .cconv import CallingConv


@dataclass
class Function:
    __match_args__ = (
        "value",
        "args",
        "blocks",
        "calling_convention",
        "global_object",
        "attrs",
    )

    # function as value
    value: Value

    # function arguments
    args: list[Value]

    # function basic blocks
    blocks: dict[str, Block]

    # A list of function attribute tuples,
    # it is worth paying attention to methods
    # {function, ret, arguments, argument}_attributes
    attrs: list[Attrs]

    calling_convention: CallingConv

    # True if function has a variable number of arguments
    # example - @printf(ptr noundef, ...)
    is_vararg: bool

    # function as global object
    global_object: GlobalObject

    def __init__(
        self,
        value: Value,
        args: list[Value],
        blocks: list[Block],
        attributes: list[tuple],
        calling_convention: int,
        is_vararg: bool,
        global_object: GlobalObject,
    ):
        self.value = value
        self.args = args
        self.blocks = {block.value.val: block for block in blocks}
        self.attrs = list(attrs_to_dict(attrs) for attrs in attributes)
        self.calling_convention = CallingConv(calling_convention)
        self.is_vararg = is_vararg
        self.global_object = global_object

    def __str__(self):
        args = ", ".join(map(str, self.args))
        blocks = "\n".join(map(str, self.blocks.values()))
        return f"define {self.value.ty} @{self.value.val}({args}) {{\n{blocks}\n}}"
