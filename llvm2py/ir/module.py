from dataclasses import dataclass
from .global_variable import GlobalVariable

from .function import Function


@dataclass
class Module:
    __match_args__ = ("funcs", "global_vars")

    # Tuple of function objects that the module contains
    funcs: list[Function]
    # A dictionary that mapf global variable names to their objects
    global_vars: dict[str, GlobalVariable]
    # A dictionary that maps function names to their objects
    funcs_map: dict[str, Function]

    def __init__(self, funcs: dict[Function], global_vars: tuple[GlobalVariable]):
        self.funcs_map = {func.value.val: func for func in funcs}
        self.funcs = funcs
        self.global_vars = {var.value.val: var for var in global_vars}

    def __str__(self):
        gvars = "\n".join(map(str, self.global_vars.values()))
        funcs = "\n".join(map(str, self.funcs))
        return gvars + "\n\n" + funcs

    def get_function(self, name: str):
        """
        Returns the function object by name
        """
        return self.funcs_map.get(name)
