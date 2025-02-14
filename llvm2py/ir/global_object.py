from enum import Enum
from typing import Tuple

from .value import Value


class LinkageType(Enum):
    ExternalLinkage = 0  # < Externally visible function
    AvailableExternallyLinkage = 1  # < Available for inspection, not emission.
    LinkOnceAnyLinkage = 2  # < Keep one copy of function when linking (inline)
    LinkOnceODRLinkage = 3  # < Same, but only replaced by something equivalent.
    WeakAnyLinkage = 4  # < Keep one copy of named function when linking (weak)
    WeakODRLinkage = 5  # < Same, but only replaced by something equivalent.
    AppendingLinkage = 6  # < Special purpose, only applies to global arrays
    InternalLinkage = 7  # < Rename collisions when linking (static functions).
    PrivateLinkage = 8  # < Like Internal, but omit from symbol table.
    ExternalWeakLinkage = 9  # < ExternalWeak linkage description.
    CommonLinkage = 10  # < Tentative definitions.


class VisibilityTypes(Enum):
    DefaultVisibility = 0  # < The GV is visible
    HiddenVisibility = 1  # < The GV is hidden
    ProtectedVisibility = 2  # < The GV is protected


class UnnamedAddr(Enum):
    Default = 0  # None
    Local = 1
    Global = 2


class GlobalObject(Value):
    # Argument position in function arguments, starting from zero
    addr_space: int  # address space of the object
    align: int
    linkage: LinkageType
    visibility: VisibilityTypes  # var visibility
    """
    If the local_unnamed_addr attribute is given,
    the address is known to not be significant within the module.
    """
    unnamed_addr: UnnamedAddr

    # See https://llvm.org/docs/LangRef.html#linkage-types
    linkage: LinkageType
    _fields = (
        "addr_space",
        "align",
        "linkage",
        "visibility",
        "unnamed_addr",
        "name",
        "type_",
    )

    def __init__(
        self,
        addr_space: int,
        align: int,
        linkage: int,
        unnamed_addr: int,
        visibility: int,
        value_args: Tuple,
    ):
        super().__init__(*value_args)
        self.addr_space = addr_space
        self.align = align
        self.linkage = LinkageType(linkage)
        self.unnamed_addr = UnnamedAddr(unnamed_addr)
        self.visibility = VisibilityTypes(visibility)

    def __repr__(self) -> str:
        return f"<GlobalObject addr_space={self.addr_space}, align={self.align}, linkage={self.linkage}, visibility={self.visibility}, unnamed_addr={self.unnamed_addr}, value_args={self.value_args}, name={self.name}, type={self.ty}, parent={self.parent.name}>"
