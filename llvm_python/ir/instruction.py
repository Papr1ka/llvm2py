from pprint import pprint, pformat
from typing import Tuple, TypeVar
from .type import Type
from .value import Value

Block = TypeVar('Block', bound='Block')


class Instruction(Value):
    __op_code: int
    __op_code_name: str
    __operands: Tuple[Value]

    _fields = (
        'op_code',
        'op_code_name',
        'operands',
        'name',
        'type_'
    )

    def __init__(self, op_code: int, op_code_name: str, operands: Tuple, value_args: Tuple):
        super().__init__(*value_args)
        self.__op_code = op_code
        self.__op_code_name = op_code_name
        self.__operands = operands

    def __str__(self):
        return (f"<llvm_python.Instruction opcode={self.__op_code}, opcode_name={self.__op_code_name},"
                f"operands={self.__operands}, type={self.type_}>")

    @property
    def op_code(self):
        return self.__op_code

    @property
    def op_code_name(self):
        return self.__op_code_name

    @property
    def operands(self):
        return self.__operands
