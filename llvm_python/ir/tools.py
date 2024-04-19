from weakref import proxy


class ParentMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _link(self, parent):
        self.parent = proxy(parent)

    def _connect(self, values):
        for value in values:
            value._link(self)


class CodeMixin:
    code: str

    def __init__(self, code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code

    def __str__(self):
        return self.code


class LinkedListMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev = None
        self.next = None

    def _setup_node(self, prev_node, next_node):
        self.prev = prev_node
        self.next = next_node


def setup_nodes(nodes):
    if len(nodes) >= 2:
        nodes[0]._setup_node(None, nodes[1])
        for i in range(1, len(nodes) - 1):
            nodes[i]._setup_node(nodes[i - 1], nodes[i + 1])
        nodes[-1]._setup_node(nodes[-2], None)
