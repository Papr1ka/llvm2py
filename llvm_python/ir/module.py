from typing import Tuple, Dict

from .function import Function
from .tools import ParentMixin, CodeMixin, setup_nodes, _queue


class Module(ParentMixin, CodeMixin):
    # Tuple of function objects that the module contains
    functions: Tuple[Function]
    # A dictionary that maps function names to their objects
    functions_map: Dict[str, Function]
    _fields = (
        'functions',
        'name',
        'type_'
    )

    def __init__(self, functions: Tuple[Function], code):
        super().__init__(code)
        self.functions_map = {function.name: function for function in functions}
        self.functions = functions
        self._connect(functions)

        setup_nodes(functions)

        # post-initialization routines
        while _queue:
            f = _queue.popleft()
            f(self)
    
    def get_function(self, name: str):
        """
        Returns the function object by name
        """
        return self.functions_map.get(name)
