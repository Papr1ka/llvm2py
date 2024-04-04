from .tools import ParentMixin, CodeMixin
from .type import Type


class Value(ParentMixin, CodeMixin):
    _name: str
    _type: Type

    _fields = (
        'name',
        'type_'
    )

    def __init__(self, name: str, type_: Type, code=None):
        super().__init__(code)
        self._name = name
        self._type = type_

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    def __repr__(self):
        t = type(self)
        return f"<{t.__module__}.{t.__qualname__} at {hex(id(self))}, name={self.name}>"
