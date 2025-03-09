from enum import Enum
from typing import Any, Union


Attrs = dict[str, Union[tuple, tuple[Any], tuple[Any, Any]]]


class CallingConv(Enum):
    """
    `Calling conventions <https://llvm.org/docs/LangRef.html#calling-conventions>`_.
    """

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
    """
    `Linkage types <https://llvm.org/docs/LangRef.html#linkage-types>`_.
    """

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
    """
    `Visibility types <https://llvm.org/docs/LangRef.html#visibility-styles>`_.
    """

    DefaultVisibility = 0  # < The GV is visible
    HiddenVisibility = 1  # < The GV is hidden
    ProtectedVisibility = 2  # < The GV is protected


class UnnamedAddr(Enum):
    """
    Unnamed addresses
    """

    Default = 0
    """
    None
    """
    Local = 1
    """
    local_unnamed_addr
    """
    Global = 2
    """
    unnamed_addr
    """


class ThreadLocal(Enum):
    """
    `Thread local storage models <https://llvm.org/docs/LangRef.html#thread-local-storage-models>`_.
    """

    NotThreadLocal = 0
    GeneralDynamicTLSModel = 1
    LocalDynamicTLSModel = 2
    InitialExecTLSModel = 3
    LocalExecTLSModel = 4


class Ordering(Enum):
    """
    `Atomic memory ordering constraints <https://llvm.org/docs/LangRef.html#atomic-memory-ordering-constraints>`_.
    """

    NotAtomic = 0
    Unordered = 1
    Monotonic = 2
    # Consume = 3
    Acquire = 4
    Release = 5
    AcquireRelease = 6
    SequentiallyConsistent = 7
