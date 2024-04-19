from .tools import ParentMixin, CodeMixin, LinkedListMixin
from .type import Type


class Value(ParentMixin, CodeMixin, LinkedListMixin):
    name: str
    type_: Type

    _fields = (
        'name',
        'type_'
    )

    def __init__(self, name: str, type_: Type, code):
        super().__init__(code)
        self.name = name
        self.type_ = type_

    def __repr__(self):
        t = type(self)
        return f"<{t.__module__}.{t.__qualname__} at\
            {hex(id(self))}, name={self.name}>"
