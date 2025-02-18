from typing import NamedTuple
from llvm2py.ir.global_object import GlobalObject

from .value import Value


class GlobalVariable(NamedTuple):
    # https://llvm.org/docs/LangRef.html#global-variables

    # global variable as value
    value: Value

    initializer: Value  # constant value

    is_const: bool  # is variable constant

    # https://llvm.org/docs/LangRef.html#global-attributes
    attributes: set[str]  # set of variable attributes

    # global variable as global object
    global_object: GlobalObject

    # https://llvm.org/docs/LangRef.html#global-variables
    is_externally_initialized: bool

    def __str__(self):
        return f"{self.value.val} = {self.initializer}"
