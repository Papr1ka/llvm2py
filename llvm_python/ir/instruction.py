from typing import Tuple, TypeVar
from .tools import setup_nodes
from .value import Value

Block = TypeVar('Block', bound='Block')


class Instruction(Value):
    op_code: int
    op_code_name: str
    operands: Tuple[Value]

    _fields = (
        'op_code',
        'op_code_name',
        'operands',
        'name',
        'type_'
    )

    def __init__(self, op_code: int, op_code_name: str, operands: Tuple[Value], value_args: Tuple):
        super().__init__(*value_args)
        self.op_code = op_code
        self.op_code_name = op_code_name
        self.operands = operands

        self._connect(operands)
        setup_nodes(operands)
