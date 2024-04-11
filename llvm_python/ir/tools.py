from weakref import proxy


class ParentMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def __init__(self, code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._code = code

    @property
    def code(self) -> str:
        return self._code

    def __str__(self):
        return self._code


class LinkedListMixin:
    def __init__(self, *args, **kwargs):
        self._prev = None
        self._next = None
        super().__init__(*args, **kwargs)

    def _setup_node(self, prev_node, next_node):
        self._prev = prev_node
        self._next = next_node

    @property
    def next(self):
        return self._next

    @property
    def prev(self):
        return self._prev


def setup_nodes(nodes):
    if len(nodes) >= 2:
        nodes[0]._setup_node(None, nodes[1])
        for i in range(1, len(nodes) - 1):
            nodes[i]._setup_node(nodes[i - 1], nodes[1 + 1])
        nodes[-1]._setup_node(nodes[-2], None)
