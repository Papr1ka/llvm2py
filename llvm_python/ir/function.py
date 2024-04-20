from typing import Tuple, Dict
from enum import Enum

from .argument import Argument
from .block import Block
from .tools import setup_nodes
from .type import Type
from .value import Value


class CallingConv(Enum):
    C = 0
    Fast = 8
    Cold = 9
    GHC = 10
    HiPE = 11
    WebKit_JS = 12
    AnyReg = 13
    PreserveMost = 14
    PreserveAll = 15
    Swift = 16
    CXX_FAST_TLS = 17
    Tail = 18
    CFGuard_Check = 19
    SwiftTail = 20
    FirstTargetCC = 64
    X86_StdCall = 64
    X86_FastCall = 65
    ARM_APCS = 66
    ARM_AAPCS = 67
    ARM_AAPCS_VFP = 68
    MSP430_INTR = 69
    X86_ThisCall = 70
    PTX_Kernel = 71
    PTX_Device = 72
    SPIR_FUNC = 75
    SPIR_KERNEL = 76
    Intel_OCL_BI = 77
    X86_64_SysV = 78
    Win64 = 79
    X86_VectorCall = 80
    HHVM = 81
    HHVM_C = 82
    X86_INTR = 83
    AVR_INTR = 84
    AVR_SIGNAL = 85
    AVR_BUILTIN = 86
    AMDGPU_VS = 87
    AMDGPU_GS = 88
    AMDGPU_PS = 89
    AMDGPU_CS = 90
    AMDGPU_KERNEL = 91
    X86_RegCall = 92
    AMDGPU_HS = 93
    MSP430_BUILTIN = 94
    AMDGPU_LS = 95
    AMDGPU_ES = 96
    AArch64_VectorCall = 97
    AArch64_SVE_VectorCall = 98
    WASM_EmscriptenInvoke = 99
    AMDGPU_Gfx = 100
    M68k_INTR = 101
    AArch64_SME_ABI_Support_Routines_PreserveMost_From_X0 = 102
    AArch64_SME_ABI_Support_Routines_PreserveMost_From_X2 = 103
    MaxID = 1023


class LinkageType(Enum):
    ExternalLinkage = 0  # < Externally visible function
    AvailableExternallyLinkage = 1  # < Available for inspection, not emission.
    LinkOnceAnyLinkage = 2  # < Keep one copy of function when linking (inline)
    LinkOnceODRLinkage = 3  # < Same, but only replaced by something equivalent.
    WeakAnyLinkage = 4  # < Keep one copy of named function when linking (weak)
    WeakODRLinkage = 5  # < Same, but only replaced by something equivalent.
    AppendingLinkage = 6  # < Special purpose, only applies to global arrays
    InternalLinkage = 7  # < Rename collisions when linking (static functions).
    PrivateLinkage = 8  # < Like Internal, but omit from symbol table.
    ExternalWeakLinkage = 9  # < ExternalWeak linkage description.
    CommonLinkage = 10  # < Tentative definitions.


class VisibilityTypes(Enum):
    DefaultVisibility = 0  # < The GV is visible
    HiddenVisibility = 1  # < The GV is hidden
    ProtectedVisibility = 2  # < The GV is protected


class Function(Value):
    # Tuple of function arguments
    args: Tuple[Argument, ...]
    # A tuple of function attribute tuples,
    # it is worth paying attention to methods
    # {function, ret, arguments, argument}_attributes
    attributes: Tuple[Tuple[str, ...], ...]
    # Tuple of block objects that the function contains
    blocks: Tuple[Block, ...]
    # A dictionary that maps block names to their objects
    blocks_map: Dict[str, Block]
    # See https://llvm.org/docs/LangRef.html#calling-conventions
    calling_convention: CallingConv
    # See https://llvm.org/docs/LangRef.html#linkage-types
    linkage_type: LinkageType
    # Type of function return value
    return_type: Type
    # Function visibility
    visibility: VisibilityTypes

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
        self.visibility = VisibilityTypes(visibility)
        self.linkage_type = LinkageType(linkage_type)
        self.calling_convention = CallingConv(calling_convention)

        self._connect(args)
        self._connect(blocks)
        setup_nodes(args)
        setup_nodes(blocks)

        for block in self.blocks:
            block._setup_pred_blocks([self.blocks_map[block_name] for block_name in block.pred_blocks_names])

    def function_attributes(self):
        """
        Returns a tuple of function attributes
        """
        return self.attributes[0]

    def ret_attributes(self):
        """
        Returns a tuple of attributes of the returned value
        """
        return self.attributes[1]

    def arguments_attributes(self):
        """
        Returns a tuple of tuples of attributes of the arguments of the function
        """
        return self.attributes[2:]

    def argument_attributes(self, arg_no: int):
        """
        Returns a tuple of the attributes of the function argument
        """
        if arg_no + 3 > len(self.attributes):
            return None
        else:
            return self.attributes[2 + arg_no]

    def get_block(self, name):
        """
        Returns the block object by name
        """
        return self.blocks_map.get(name)
