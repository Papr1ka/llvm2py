from enum import Enum

from dataclasses import dataclass
from xml.dom.minidom import Attr

from .global_object import GlobalObject

from .block import Block
from .value import Value
from .instruction import Attrs


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


@dataclass
class Function:
    __match_args__ = (
        "value",
        "args",
        "blocks",
        "calling_convention",
        "global_object",
        "attrs",
    )

    # function as value
    value: Value

    # function arguments
    args: list[Value]

    # function basic blocks
    blocks: list[Block]

    # A list of function attribute tuples,
    # it is worth paying attention to methods
    # {function, ret, arguments, argument}_attributes
    attrs: list[Attrs]

    calling_convention: CallingConv

    # function as global object
    global_object: GlobalObject

    def __init__(
        self,
        value: Value,
        args: list[Value],
        blocks: list[Block],
        attrs: list[Attrs],
        calling_convention: int,
        global_object: GlobalObject,
    ):
        self.value = value
        self.args = args
        self.blocks = blocks
        self.attrs = list(set(attrs) for attrs in attrs)
        self.calling_convention = CallingConv(calling_convention)
        self.global_object = global_object

    def __str__(self):
        args = ", ".join(map(str, self.args))
        blocks = "\n".join(map(str, self.blocks))
        return f"define {self.value.ty} @{self.value.val}({args}) {{\n{blocks}\n}}"
