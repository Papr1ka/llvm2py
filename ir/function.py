from typing import Tuple
from .block import Block
from .type import Type


class Function:
    name: str
    return_type: Type
    args: tuple
    blocks: Tuple[Block]

    def __str__(self):
        return f"<Function name={self.name}, return_type={self.return_type}, args={self.args}, blocks=..."

    def __repr__(self):
        return f"<Function name={self.name}>"
