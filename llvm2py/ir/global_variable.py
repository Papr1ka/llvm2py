from enum import Enum
from typing import Tuple, Union

from llvm2py.ir.function import LinkageType, VisibilityTypes
from llvm2py.ir.global_object import GlobalObject

from .value import Value


class GlobalVariable(GlobalObject):
    # https://llvm.org/docs/LangRef.html#global-variables

    # https://llvm.org/docs/LangRef.html#global-attributes
    attributes: set[str]  # set of variable attributes

    initializer: Value  # constant value
    is_const: bool  # is variable constant

    """
    By default, global initializers are optimized by assuming that
    global variables defined within the module are not modified from
    their initial values before the start of the global initializer.
    This is true even for variables potentially accessible
    from outside the module, including those with
    external linkage or appearing in @llvm.used or dllexported variables.
    This assumption may be suppressed by marking the variable with externally_initialized.
    """
    is_externally_initialized: bool

    _fields = (
        "addr_space",
        "attributes",
        "initializer",
        "is_const",
        "is_externally_initialized",
        "linkage",
        "unnamed_addr",
        "visibility",
        "name",
        "type_",
    )

    def __init__(
        self,
        # addr_space: int,
        attributes: Tuple[str],
        initializer_args: Tuple,
        is_const: bool,
        is_externally_initialized: bool,
        # linkage: int,
        # unnamed_addr: int,
        # visibility: int,
        global_object_args: Tuple,
        value_args: Tuple,
    ):
        super().__init__(*global_object_args, value_args)
        self.attributes = attributes
        self.initializer = Value(*initializer_args)
        self.is_const = is_const
        self.is_externally_initialized = is_externally_initialized

    def __repr__(self) -> str:
        return f"<GlobalVariable addr_space={self.addr_space}, attributes={self.attributes}, \
initializer={self.initializer}, is_const={self.is_const}, \
is_externally_initialized={self.is_externally_initialized}, \
linkage={self.linkage}, unnamed_addr={self.unnamed_addr}, \
visibility={self.visibility}, type={self.ty}>"
