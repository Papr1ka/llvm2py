from typing import Tuple, TypeVar, List, Self

from .tools import setup_nodes
from .value import Value
from .instruction import Instruction

Function = TypeVar('Function', bound='Function')


class Block(Value):
    _instructions: Tuple[Instruction]
    _fields = (
        'instructions',
        'name',
        'pred_blocks_names',
        'type_'
    )

    def __init__(self, instructions, pred_blocks: Tuple[str], value_args: Tuple):
        super().__init__(*value_args)
        self._instructions = instructions
        self._pred_blocks_names = pred_blocks
        self._connect(instructions)
        setup_nodes(instructions)
        self._pred_blocks = None

    @property
    def instructions(self):
        return self._instructions

    @property
    def pred_blocks_names(self):
        return self._pred_blocks_names

    @property
    def pred_blocks(self):
        return self._pred_blocks

    def _setup_pred_blocks(self, blocks: List[Self]):
        self._pred_blocks = blocks
