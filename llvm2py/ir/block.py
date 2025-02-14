from typing import Tuple, List

from .instruction import Instruction
from .value import Value


class Block(Value):
    # Tuple of instruction objects that the block contains
    instrs: Tuple[Instruction, ...]

    # Tuple of predecessor block names
    pred_blocks: Tuple[str, ...]
    _fields = ("instrs", "pred_blocks", "name", "type_")

    def __init__(self, instrs, pred_blocks: Tuple[str, ...], value_args: Tuple):
        super().__init__(*value_args)
        self.instrs = instrs
        self.pred_blocks = pred_blocks
