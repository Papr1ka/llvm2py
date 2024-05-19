from typing import Tuple, Dict, Any
from enum import Enum

from .tools import setup_nodes, _queue
from .value import Value


class Opcode(Enum):
    Invalid = 0
    
    # Term instructions
    Ret = 1
    Br = 2
    Switch = 3
    IndirectBr = 4
    Invoke = 5
    Resume = 6
    Unreachable = 7
    CleanupRet = 8
    CatchRet = 9
    CatchSwitch = 10
    CallBr = 11  # A call-site terminator
    
    # Unary operators
    FNeg = 12
    
    # Binary operators
    Add = 13
    FAdd = 14
    Sub = 15
    FSub = 16
    Mul = 17
    FMul = 18
    UDiv = 19
    SDiv = 20
    FDiv = 21
    URem = 22
    SRem = 23
    FRem = 24
    
    # Logical operators
    Shl = 25  # Shift left  (logical)
    LShr = 26  # Shift right (logical)
    AShr = 27  # Shift right (arithmetic)
    And = 28
    Or = 29
    Xor = 30
    
    # Memory operators
    Alloca = 31  # Stack management
    Load = 32  # Memory manipulation instrs
    Store = 33
    GetElementPtr = 34
    Fence = 35
    AtomicCmpXchg = 36
    AtomicRMW = 37
    
    # Cast operators
    Trunc = 38  # Truncate integers
    ZExt = 39  # Zero extend integers
    SExt = 40  # Sign extend integers
    FPToUI = 41  # floating point -> UInt
    FPToSI = 42  # floating point -> SInt
    UIToFP = 43  # UInt -> floating point
    SIToFP = 44  # SInt -> floating point
    FPTrunc = 45  # Truncate floating point
    FPExt = 46  # Extend floating point
    PtrToInt = 47  # Pointer -> Integer
    IntToPtr = 48  # Integer -> Pointer
    BitCast = 49  # Type cast
    AddrSpaceCast = 50  # addrspace cast
    
    CleanupPad = 51
    CatchPad = 52
    
    # Other instructions
    ICmp = 53  # Integer comparison instruction
    FCmp = 54  # Floating point comparison instr.
    PHI = 55  # PHI node instruction
    Call = 56  # Call a function
    Select = 57  # select instruction
    UserOp1 = 58  # May be used internally in a pass
    UserOp2 = 59  # Internal to passes only
    VAArg = 60  # vaarg instruction
    ExtractElement = 61  # extract from vector
    InsertElement = 62  # insert into vector
    ShuffleVector = 63  # shuffle two vectors.
    ExtractValue = 64  # extract from aggregate
    InsertValue = 65  # insert into aggregate
    LandingPad = 66  # Landing pad instruction.
    Freeze = 67  # Freeze instruction.


class Instruction(Value):
    # Instruction opcode
    op_code: Opcode
    # Instruction opcode name
    op_code_name: str
    # Tuple of operand instruction operands
    operands: Tuple[Value, ...]
    """
    Additional data, different for each instruction
    
    If instruction is {}, than additional data will be ...
    
    Alloca:
        AllocatedType: Type
        Align: int
    
    GetElementPtr:
        SourceElementType: Type
        ResultElementType: Type
        Indices: Tuple[Value]
    """
    additional_data: Dict[str, Any]

    _fields = (
        'op_code',
        'op_code_name',
        'operands',
        'data',
        'name',
        'type_',
    )

    def __init__(self, op_code: int, op_code_name: str, operands: Tuple[Value], data, value_args: Tuple):
        super().__init__(*value_args)
        self.op_code = Opcode(op_code)
        self.op_code_name = op_code_name
        self.additional_data = data

        for i, operand in enumerate(operands):
            if operand.name.startswith("llvm."):
                # intrinsic, must be a function instead of a value
                def swap_later(module):
                    new_operands = [*self.operands[:i],
                                    module.get_function(self.operands[i].name),
                                    *self.operands[i + 1:]]
                    self.operands = tuple(new_operands)
                _queue.append(swap_later)

        self.operands = operands

        self._connect(operands)
        setup_nodes(operands)
