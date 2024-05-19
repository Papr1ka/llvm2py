from typing import Tuple, List

from .instruction import Instruction
from .tools import setup_nodes
from .value import Value


class Block(Value):
    # Tuple of instruction objects that the block contains
    instructions: Tuple[Instruction, ...]
    _fields = (
        'instructions',
        'name',
        'pred_blocks_names',
        'type_'
    )

    def __init__(self, instructions, pred_blocks_names: Tuple[str, ...], value_args: Tuple):
        super().__init__(*value_args)
        self.instructions = instructions
        self.pred_blocks_names = pred_blocks_names
        self.pred_blocks = None
        
        self._connect(instructions)
        setup_nodes(instructions)

    def _setup_pred_blocks(self, blocks: List):
        self.pred_blocks = blocks
