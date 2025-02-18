from typing import NamedTuple
from .instruction import Instruction
from .value import Value


class Block(NamedTuple):
    # block as value
    value: Value

    # block instructions
    instrs: list[Instruction]

    # predecessor block names
    pred_blocks: list[str]

    def __str__(self):
        return f"{self.value.val}:\n\t" + "\n\t".join(map(str, self.instrs))
