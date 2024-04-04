from typing import Tuple
from .block import Block
from .type import Type
from .argument import Argument
from .value import Value


class Function(Value):
    _args: Tuple[Argument]
    _attributes: Tuple[Tuple[str]]
    _blocks: Tuple[Block]
    _calling_convention: int
    _linkage_type: int
    _return_type: Type
    _visibility: int

    _fields = (
        'args',
        'attributes',
        'blocks',
        'calling_convention',
        'linkage_type',
        'visibility',
        'return_type',
        'name',
        'type_'
    )

    def __init__(self, args, blocks, attributes, return_type, visibility, linkage_type, calling_convention, value_args: Tuple):
        super().__init__(*value_args)
        self._args = args
        self._blocks = blocks
        self._attributes = attributes
        self._return_type = return_type
        self._visibility = visibility
        self._linkage_type = linkage_type
        self._calling_convention = calling_convention

        self._connect(args)
        self._connect(blocks)

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
        return self._args

    @property
    def attributes(self):
        return self._attributes

    @property
    def blocks(self):
        return self._blocks

    @property
    def return_type(self):
        return self._return_type

    @property
    def visibility(self):
        return self._visibility

    @property
    def linkage_type(self):
        return self._linkage_type

    @property
    def calling_convention(self):
        return self._calling_convention
