from pprint import pprint, pformat

from .type import Type


class Value:
    __name: str
    __type: Type

    _fields = (
        'name',
        'type_'
    )

    def __init__(self, name: str, type_: Type):
        self.__name = name
        self.__type = type_

    @property
    def name(self):
        return self.__name

    @property
    def type_(self):
        return self.__type

    def __str__(self):
        return f"<llvm_python.Value name={self.__name}, type={self.__type}>"
