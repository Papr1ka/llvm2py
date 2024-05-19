from weakref import proxy
from collections import deque


_queue = deque()  # queue for module post-initialization routines


class ParentMixin:
    """
    The class adds functionality to support backward references
    to the parent

    e.g. the parent of an instruction will point to the block containing it
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _link(self, parent):
        self.parent = proxy(parent)

    def _connect(self, values):
        for value in values:
            value._link(self)


class CodeMixin:
    """
    The class provides a field to store the code
    that the class is associated with for beautiful __str__ output
    """
    code: str

    def __init__(self, code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code

    def __str__(self):
        return self.code


class LinkedListMixin:
    """
    The class implements the principle of a doubly-linked list
    If you have blocks [%1, %2, %3], then prev of block %2
    will point to the object of block %1,
    and next to the object of block %3,
    do not confuse prev and pred_blocks.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev = None
        self.next = None

    def _setup_node(self, prev_node, next_node):
        self.prev = prev_node
        self.next = next_node


def setup_nodes(nodes):
    """
    Sets item references for a doubly linked list
    """
    if len(nodes) >= 2:
        nodes[0]._setup_node(None, nodes[1])
        for i in range(1, len(nodes) - 1):
            nodes[i]._setup_node(nodes[i - 1], nodes[i + 1])
        nodes[-1]._setup_node(nodes[-2], None)
