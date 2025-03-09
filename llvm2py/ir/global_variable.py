from dataclasses import dataclass

from .global_object import GlobalObject
from .enum import Attrs
from .support import attrs_to_dict
from .value import Value


@dataclass
class GlobalVariable:
    """
    `GlobalVariable class <https://llvm.org/docs/LangRef.html#global-variables>`_.
    """

    value: Value
    """
    Global variable as value
    """

    initializer: Value
    """
    A constant value that the global variable takes on during initialization.
    """

    is_const: bool
    """
    If True, varialbe is marked as a constant.
    """

    attrs: Attrs
    """
    Global variable attributes.
    """

    global_object: GlobalObject
    """
    Global variable as global object.
    """

    is_externally_initialized: bool
    """
    If True, variable is marked as ExternallyInitialized.
    """

    def __init__(
        self,
        value,
        initializer,
        is_const,
        attributes,
        global_object,
        is_externally_initialized,
    ):
        self.value = value
        self.initializer = initializer
        self.is_const = is_const
        self.attrs = attrs_to_dict(attributes)
        self.global_object = global_object
        self.is_externally_initialized = is_externally_initialized
