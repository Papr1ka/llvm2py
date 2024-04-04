from typing import TypeVar, Tuple

from .value import Value

Function = TypeVar('Function', bound='Function')


class Argument(Value):
    _position: int
    _fields = (
        'position',
        'name',
        'type_'
    )

    def __init__(self, position, value_args: Tuple):
        super().__init__(*value_args)
        self._position = position

    def __str__(self) -> str:
        return f"<Argument position={self.position}, name={self.name}, type={self.type}, parent={self.__function}>"

    @property
    def position(self):
        return self._position
