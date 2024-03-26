from pprint import pprint, pformat
from typing import TypeVar, Tuple
from .value import Value

Function = TypeVar('Function', bound='Function')


class Argument(Value):
    __position: int
    _fields = (
        'position',
        'name',
        'type_'
    )

    def __init__(self, position, value_args: Tuple):
        super().__init__(*value_args)
        self.__position = position

    def __str__(self) -> str:
        return f"<Argument position={self.position}, name={self.name}, type={self.type}, parent={self.__function}>"

    @property
    def name(self):
        return self.__name

    @property
    def position(self):
        return self.__position

    @property
    def type(self):
        return self.__type
