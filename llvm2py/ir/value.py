from .tools import ParentMixin, CodeMixin, LinkedListMixin
from .type import Type


class Value(ParentMixin, CodeMixin, LinkedListMixin):
    """
    Name or presentation as operand

    Constant int value 42 will have name 42
    Value name can be 1.500000e+01, -2.700000e+01, 0x4080133340000000
    Block with name %8 will have name %8
    """
    name: str
    type_: Type

    _fields = (
        'name',
        'type_'
    )

    def __init__(self, name: str, type_: Type, code) -> None:
        super().__init__(code)
        self.name = name
        self.type_ = type_

    def __repr__(self) -> str:
        t = type(self)
        return f"<{t.__module__}.{t.__qualname__} at\
{hex(id(self))}, name={self.name}>"
