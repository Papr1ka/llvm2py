from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


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


@dataclass
class GlobalObject:
    """
    Class, representing GlobalObject and GlobalValue fields
    """

    addr_space: int  # address space of the object
    align: int  # alignment of the object
    linkage: LinkageType  # object linkage type
    visibility: VisibilityTypes  # object visibility

    """
    If the local_unnamed_addr attribute is given,
    the address is known to not be significant within the module.
    """
    unnamed_addr: UnnamedAddr

    def __init__(
        self,
        addr_space: int,
        align: int,
        linkage: int,
        visibility: int,
        unnamed_addr: int,
    ):
        self.addr_space = addr_space
        self.align = align
        self.linkage = LinkageType(linkage)
        self.unnamed_addr = UnnamedAddr(unnamed_addr)
        self.visibility = VisibilityTypes(visibility)
