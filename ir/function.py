from typing import Tuple
from .block import Block
from .type import Type
from .argument import Argument
from .attribute import Attribute


class Function:
    name: str
    return_type: Type
    args: Tuple[Argument]
    blocks: Tuple[Block]
    attributes: Tuple[Tuple[Attribute]]

    def __str__(self):
        return f"<Function name={self.name}, return_type={self.return_type}, args={self.args}, attributes={self.attributes}, blocks=..."

    def __repr__(self):
        return f"<Function name={self.name}>"

    def get_function_attributes(self):
        return self.attributes[0]

    def get_ret_attributes(self):
        return self.attributes[1]

    def get_arguments_attributes(self):
        return self.attributes[2:]

    def get_argument_attribute(self, arg_no: int):
        if len(self.attributes) - 2 < arg_no:
            return None