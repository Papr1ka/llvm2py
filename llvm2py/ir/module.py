from typing import Tuple, Dict

from llvm2py.ir.global_variable import GlobalVariable

from .function import Function
from .tools import CodeMixin


class Module(CodeMixin):
    __match_args__ = ("funcs", "global_vars")
    _fields = ("funcs", "global_variables", "name", "ty")

    # Tuple of function objects that the module contains
    funcs: Tuple[Function]
    # A dictionary that maps function names to their objects
    funcs_map: Dict[str, Function]
    # A dictionary that mapf global variable names to their objects
    global_vars: Dict[str, GlobalVariable]

    def __init__(
        self, funcs: Tuple[Function], global_vars: Tuple[GlobalVariable], code
    ):
        super().__init__(code)
        self.funcs_map = {func.name: func for func in funcs}
        self.funcs = funcs
        self.global_vars = {var.name: var for var in global_vars}

    def get_function(self, name: str):
        """
        Returns the function object by name
        """
        return self.funcs_map.get(name)
