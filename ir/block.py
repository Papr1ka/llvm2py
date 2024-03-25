from typing import Tuple
from .function import Function

class Block:
    name: str
    instructions: Tuple[str]
    function: Function

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
