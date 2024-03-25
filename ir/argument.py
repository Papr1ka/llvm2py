from typing import TypeVar

from .type import Type

Function = TypeVar('Function', bound='Function')


class Argument:
    position: int
    name: str
    type: Type
    function: Function

    def __str__(self) -> str:
        return f"<Argument position={self.position}, name={self.name}, type={self.type}, parent={self.parent}>"
