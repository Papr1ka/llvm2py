from typing import Tuple, Iterator

from .instruction import Instruction
from .block import Block
from .tools import setup_nodes
from .type import Type
from .argument import Argument
from .value import Value


class Function(Value):
    _args: Tuple[Argument]
    _attributes: Tuple[Tuple[str]]
    _blocks_tuple: Tuple[Block]
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

    def __init__(self, args, blocks, attributes, return_type, visibility, linkage_type, calling_convention,
                 value_args: Tuple):
        super().__init__(*value_args)
        self._args = args
        self._blocks_tuple = blocks
        self._blocks = {block.name: block for block in blocks}
        self._attributes = attributes
        self._return_type = return_type
        self._visibility = visibility
        self._linkage_type = linkage_type
        self._calling_convention = calling_convention

        self._connect(args)
        self._connect(blocks)
        setup_nodes(args)
        setup_nodes(blocks)

        for block in self.blocks:
            block._setup_pred_blocks([self._blocks[block_name] for block_name in block.pred_blocks_names])

    def get_function_attributes(self) -> Tuple[str]:
        return self.attributes[0]

    def get_ret_attributes(self) -> Tuple[str]:
        return self.attributes[1]

    def get_arguments_attributes(self) -> Tuple[Tuple[str]]:
        return self.attributes[2:]

    def get_argument_attributes(self, arg_no: int) -> Tuple[str]:
        if arg_no + 3 > len(self.attributes):
            return None
        else:
            return self.attributes[2 + arg_no]

    @property
    def args(self) -> Tuple[Argument]:
        return self._args

    @property
    def attributes(self) -> Tuple[Tuple[str]]:
        return self._attributes

    @property
    def blocks(self) -> Tuple[Block]:
        return self._blocks_tuple

    @property
    def return_type(self) -> Type:
        return self._return_type

    @property
    def visibility(self) -> int:
        return self._visibility

    @property
    def linkage_type(self) -> int:
        return self._linkage_type

    @property
    def calling_convention(self) -> int:
        return self._calling_convention

    def get_block(self, name) -> Block:
        return self._blocks.get(name)

    def instruction_iterator(self) -> Iterator[Instruction]:
        for block in self._blocks_tuple:
            for instruction in block.instructions:
                yield instruction

    @property
    def instructions(self) -> Tuple[Instruction, ...]:
        return tuple(self.instruction_iterator())
