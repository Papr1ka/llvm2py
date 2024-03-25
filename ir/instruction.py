from typing import Tuple
from .block import Block
from .type import Type


class Instruction:
    parent_block: Block
    op_code: int
    op_code_name: str
    operands: Tuple
    type: Type
