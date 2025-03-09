from dataclasses import dataclass
from .enum import LinkageType, VisibilityTypes, UnnamedAddr, ThreadLocal


@dataclass
class GlobalObject:
    """
    Class, representing GlobalObject and GlobalValue fields.
    """

    addr_space: int
    """
    Address space of the object.
    """

    align: int
    """
    Alignment of the object.
    """

    linkage: LinkageType
    """
    Object linkage type.
    """

    visibility: VisibilityTypes
    """
    Object visibility.
    """

    unnamed_addr: UnnamedAddr
    """
    Object UnnamedAddr.
    If the local_unnamed_addr attribute is given,
    the address is known to not be significant within the module.
    """

    thread_local: ThreadLocal
    """
    Object ThreadLocal model.
    """

    section: str | None
    """
    Object section.
    """

    def __init__(
        self,
        addr_space: int,
        align: int,
        linkage: int,
        unnamed_addr: int,
        visibility: int,
        thread_local: int,
        section: str,
    ):
        self.addr_space = addr_space
        self.align = align
        self.linkage = LinkageType(linkage)
        self.unnamed_addr = UnnamedAddr(unnamed_addr)
        self.visibility = VisibilityTypes(visibility)
        self.thread_local = ThreadLocal(thread_local)
        self.section = section if len(section) > 0 else None
