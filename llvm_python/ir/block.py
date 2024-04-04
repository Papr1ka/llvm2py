from typing import Tuple, TypeVar
from .value import Value
from .instruction import Instruction


Function = TypeVar('Function', bound='Function')


class Block(Value):
    _instructions: Tuple[Instruction]
    _fields = (
        'instructions',
        'name',
        'type_'
    )

    def __init__(self, instructions, value_args: Tuple):
        super().__init__(*value_args)
        self._instructions = instructions

        self._connect(instructions)

    @property
    def instructions(self):
        return self._instructions
