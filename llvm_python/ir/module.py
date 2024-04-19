from typing import Tuple, Dict, Union

from .block import Block
from .instruction import Instruction
from .function import Function
from .tools import ParentMixin, CodeMixin, setup_nodes


class Module(ParentMixin, CodeMixin):
    functions: Tuple[Function]
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
    
    def get_function(self, name: str) -> Union[Function, None]:
        return self.functions_map.get(name)
