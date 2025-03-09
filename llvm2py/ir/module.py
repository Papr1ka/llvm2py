from dataclasses import dataclass
from .global_variable import GlobalVariable

from .function import Function


@dataclass
class Module:
    """
    Module class coresponds to the llvm module class.
    """

    funcs: dict[str, Function]
    """
    A dictionary that maps function names to their objects.
    """

    global_vars: dict[str, GlobalVariable]
    """
    A dictionary that maps global variable names to their objects.
    """

    def __init__(self, funcs: list[Function], global_vars: tuple[GlobalVariable]):
        self.funcs = {func.value.val: func for func in funcs}
        self.global_vars = {var.value.val: var for var in global_vars}
