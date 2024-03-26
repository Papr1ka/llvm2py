from pprint import pprint, pformat
from typing import Tuple
from .block import Block
from .type import Type
from .argument import Argument
from .value import Value


class Function(Value):
    __args: Tuple[Argument]
    __attributes: Tuple[Tuple[str]]
    __blocks: Tuple[Block]
    __calling_convention: int
    __linkage_type: int
    __return_type: Type
    __visibility: int

    _fields = (
        'args',
        'attributes',
        'blocks',
        'calling_convention',
        'linkage_type',
        'visibility',
        'name',
        'type_'
    )

    def __init__(self, args, blocks, attributes, return_type, visibility, linkage_type, calling_convention, value_args: Tuple):
        super().__init__(*value_args)
        self.__args = args
        self.__blocks = blocks
        self.__attributes = attributes
        self.__return_type = return_type
        self.__visibility = visibility
        self.__linkage_type = linkage_type
        self.__calling_convention = calling_convention

    def __str__(self):
        return f"<Function name={self.name}, return_type={self.__return_type}, args={self.__args}, attributes={self.__attributes}, blocks=..."

    def get_function_attributes(self):
        return self.attributes[0]

    def get_ret_attributes(self):
        return self.attributes[1]

    def get_arguments_attributes(self):
        return self.attributes[2:]

    def get_argument_attributes(self, arg_no: int):
        if arg_no + 3 > len(self.attributes):
            return None
        else:
            return self.attributes[2 + arg_no]

    @property
    def args(self):
        return self.__args

    @property
    def attributes(self):
        return self.__attributes

    @property
    def blocks(self):
        return self.__blocks

    @property
    def return_type(self):
        return self.__return_type

    @property
    def visibility(self):
        return self.__visibility

    @property
    def linkage_type(self):
        return self.__linkage_type

    @property
    def calling_convention(self):
        return self.__calling_convention
