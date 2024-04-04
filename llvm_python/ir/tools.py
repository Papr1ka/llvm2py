from weakref import proxy


class ParentMixin:

    def _link(self, parent):
        assert parent is not None
        self._parent = proxy(parent)

    def _connect(self, values):
        for value in values:
            value._link(self)

    @property
    def parent(self):
        return self._parent


class CodeMixin:
    _code: str

    def __init__(self, code: str):
        self._code = code

    @property
    def code(self):
        return self._code

    def __str__(self):
        return self._code
