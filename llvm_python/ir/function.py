from typing import Tuple, Iterator, Dict, Union

from .instruction import Instruction
from .block import Block
from .tools import setup_nodes
from .type import Type
from .argument import Argument
from .value import Value


class Function(Value):
    args: Tuple[Argument, ...]
    attributes: Tuple[Tuple[str, ...], ...]
    blocks: Tuple[Block, ...]
    blocks_map: Dict[str, Block]
    calling_convention: int
    linkage_type: int
    return_type: Type
    visibility: int

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

    def __init__(self, args, blocks, attributes, return_type, visibility, linkage_type,
                 calling_convention, value_args: Tuple):
        super().__init__(*value_args)
        self.args = args
        self.blocks = blocks
        self.blocks_map = {block.name: block for block in blocks}
        self.attributes = attributes
        self.return_type = return_type
        self.visibility = visibility
        self.linkage_type = linkage_type
        self.calling_convention = calling_convention

        self._connect(args)
        self._connect(blocks)
        setup_nodes(args)
        setup_nodes(blocks)

        for block in self.blocks:
            block._setup_pred_blocks([self.blocks_map[block_name] for block_name in block.pred_blocks_names])

    def function_attributes(self) -> Tuple[str, ...]:
        return self.attributes[0]

    def ret_attributes(self) -> Tuple[str, ...]:
        return self.attributes[1]

    def arguments_attributes(self) -> Tuple[Tuple[str, ...], ...]:
        return self.attributes[2:]

    def argument_attributes(self, arg_no: int) -> Union[Tuple[str, ...], None]:
        if arg_no + 3 > len(self.attributes):
            return None
        else:
            return self.attributes[2 + arg_no]

    def get_block(self, name) -> Union[Block, None]:
        return self.blocks_map.get(name)
