from pprint import pprint, pformat
from typing import Tuple, TypeVar

from .value import Value
from .instruction import Instruction

Function = TypeVar('Function', bound='Function')


class Block(Value):
    __instructions: Tuple[Instruction]
    _fields = (
        'instructions',
        'name',
        'type_'
    )

    def __init__(self, instructions, value_args: Tuple):
        super().__init__(*value_args)
        self.__instructions = instructions

    def __str__(self):
        return self.__name

    @property
    def instructions(self):
        return self.__instructions
