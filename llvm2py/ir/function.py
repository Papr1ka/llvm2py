from dataclasses import dataclass

from .support import attrs_list_to_dict

from .global_object import GlobalObject

from .block import Block
from .value import Value
from .enum import CallingConv, Attrs


@dataclass
class Function:
    """
    Function class
    """

    value: Value
    """
    Function as value.
    """

    args: list[Value]
    """
    List of function arguments.
    """

    # function basic blocks
    blocks: dict[str, Block]
    """
    A dictionary that maps block names to their objects.
    """

    attrs: list[Attrs]
    """
    A list of function attributes.
    Each element references either the function itself, the return value, or one of the arguments.
    
    For convenience, you can use functions from the support module to extract attributes.
    """

    calling_convention: CallingConv
    """
    Function calling convention.
    """

    is_vararg: bool
    """
    If True, the function has a variable number of arguments.
    For example - @printf(ptr noundef, ...).
    """

    global_object: GlobalObject
    """
    Function as global object.
    """

    def __init__(
        self,
        value: Value,
        args: list[Value],
        blocks: list[Block],
        attributes: list[list[tuple]],
        calling_convention: int,
        is_vararg: bool,
        global_object: GlobalObject,
    ):
        self.value = value
        self.args = args
        self.blocks = {block.value.val: block for block in blocks}
        self.attrs = attrs_list_to_dict(attributes)
        self.calling_convention = CallingConv(calling_convention)
        self.is_vararg = is_vararg
        self.global_object = global_object

    def has_no_body(self):
        """
        Returns true if the function is only declared but not defined.
        """
        return len(self.blocks) == 0
