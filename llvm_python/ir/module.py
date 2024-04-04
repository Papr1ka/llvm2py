from typing import Tuple, Dict, Iterator

from .block import Block
from .instruction import Instruction
from .function import Function
from .tools import ParentMixin, CodeMixin, setup_nodes


class Module(ParentMixin, CodeMixin):
    _functions: Dict[str, Function]
    _functions_tuple: Tuple[Function]
    _fields = (
        'functions',
        'name',
        'type_'
    )

    def __init__(self, functions: Tuple[Function], code):
        super().__init__(code)
        self._functions = {function.name: function for function in functions}
        self._functions_tuple = functions
        self._connect(functions)

        setup_nodes(functions)

    def get_function(self, name: str) -> Function:
        return self._functions.get(name)

    @property
    def functions(self) -> Tuple[Function]:
        return self._functions_tuple

    def block_iterator(self) -> Iterator[Block]:
        for function in self._functions_tuple:
            for block in function.blocks:
                yield block

    @property
    def blocks(self) -> Tuple[Block, ...]:
        return tuple(self.block_iterator())

    def instruction_iterator(self) -> Iterator[Instruction]:
        for block in self.block_iterator():
            for instruction in block.instructions:
                yield instruction

    @property
    def instructions(self) -> Tuple[Instruction, ...]:
        return tuple(self.instruction_iterator())
