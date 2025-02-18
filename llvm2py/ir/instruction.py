from dataclasses import dataclass
from typing import Any

from .type import Type
from .value import Value

Attr = tuple  # (str,) (str, Any) (str, Any, Any...)
Attrs = set[Attr]


@dataclass(frozen=True)
class Instruction:
    # instruction attributes
    attrs: Attrs

    # instruction as value
    result: Value

    # instruction opcode
    opcode: str


@dataclass(frozen=True)
class CallInstr(Instruction):
    call_attributes: list[Attrs]


@dataclass(frozen=True)
class UserInstructionContainer(Instruction):
    operands: list[Value]


@dataclass(frozen=True)
class Ret(Instruction):
    value: Value

    def __str__(self):
        return f"ret {self.value}"


@dataclass(frozen=True)
class Br(Instruction):
    cond: Value | None
    label_false: Value  # stores label, if Br is unconditional
    label_true: Value | None

    def __str__(self):
        if self.cond is not None:
            return f"br {self.cond}, {self.label_true}, {self.label_false}"
        else:
            return f"br {self.label_false}"


@dataclass(frozen=True)
class Switch(Instruction):
    cond: Value
    label_default: Value
    cases: list[tuple[Value, Value]]  # [(cond, label)]

    def __str__(self):
        return f"switch {self.cond}, {self.label_default}" + (
            f"[{' '.join(f'{case}, {label}' for case, label in self.cases)}]"
        )


@dataclass(frozen=True)
class IndirectBr(Instruction):
    addr: Value
    possible_dests: list[Value]

    def __str__(self):
        return f"indirectbr {self.addr}, [{', '.join(map(str, self.possible_dests))}]"


@dataclass(frozen=True)
class Invoke(CallInstr):
    func: Value
    args: list[Value]
    label_ok: Value
    label_err: Value

    def __str__(self):
        return (
            f"{self.result} = invoke {self.func}({', '.join(map(str, self.args))}) "
            + (f"to {self.label_ok} unwind {self.label_err}")
        )


@dataclass(frozen=True)
class Resume(Instruction):
    val: Value

    def __str__(self):
        return f"resume {self.val}"


@dataclass(frozen=True)
class CallBr(CallInstr):
    callee: Value
    args: list[Value]
    fallthrough_label: Value
    indirect_labels: list[Value]

    def __str__(self):
        return (
            f"{self.result} = callbr {self.callee}({', '.join(map(str, self.args))}) "
            + (
                f"{self.fallthrough_label} [{', '.join(map(str, self.indirect_labels))}]"
            )
        )


@dataclass(frozen=True)
class CatchSwitch(Instruction):
    parent: Value
    handler_labels: list[Value]  # list of labels
    label_default: Value | None

    def __str__(self):
        caller = "caller" if self.label_default is None else self.label_default
        return f"{self.result} = catchswitch within {self.parent}" + (
            f"[{', '.join(map(str, self.handler_labels))}] unwind to {caller}"
        )


@dataclass(frozen=True)
class CatchRet(Instruction):
    catch: Value
    succ_label: Value

    def __str__(self):
        return f"catchret from {self.catch} to {self.succ_label}"


@dataclass(frozen=True)
class CleanupRet(Instruction):
    cleanup: Value
    succ_label: Value

    def __str__(self):
        return f"cleanup from {self.cleanup} to {self.succ_label}"


@dataclass(frozen=True)
class Unreacheble(Instruction):
    def __str__(self):
        return "unreachable"


@dataclass(frozen=True)
class UnaryOp(Instruction):
    operand: Value

    def __str__(self):
        return f"{self.result} = {self.opcode} {self.operand}"


@dataclass(frozen=True)
class BinOp(Instruction):
    fst_operand: Value
    snd_operand: Value

    def __str__(self):
        return f"{self.result} = {self.opcode} {self.fst_operand}, {self.snd_operand}"


@dataclass(frozen=True)
class ExtractElement(Instruction):
    vector: Value
    index: Value

    def __str__(self):
        return f"{self.result} = extractelement {self.vector}, {self.index}"


@dataclass(frozen=True)
class InsertElement(Instruction):
    vector: Value
    value: Value
    index: Value

    def __str__(self):
        return (
            f"{self.result} = insertelement {self.vector}, {self.value}, {self.index}"
        )


@dataclass(frozen=True)
class ShuffleVector(Instruction):
    fst_vector: Value
    snd_vector: Value
    mask_vector: Value

    def __str__(self):
        return f"{self.result} = shufflevector {self.fst_vector}, {self.snd_vector}, {self.mask_vector}"


@dataclass(frozen=True)
class ExtractValue(Instruction):
    aggregate: Value
    indices: list[int]

    def __str__(self):
        return f"{self.result} = extractvalue {self.aggregate}, " + (
            f"{', '.join(map(str, self.indices))}"
        )


@dataclass(frozen=True)
class InsertValue(Instruction):
    aggregate: Value
    value: Value
    indices: list[int]

    def __str__(self):
        return f"{self.result} = insertvalue {self.aggregate}, {self.value}, " + (
            f"{', '.join(map(str, self.indices))}"
        )


@dataclass(frozen=True)
class Alloca(Instruction):
    num_elements: Value
    allocated_ty: Type

    def __str__(self):
        return f"{self.result} = alloca {self.allocated_ty}, {self.num_elements}"


@dataclass(frozen=True)
class Load(Instruction):
    address: Value

    def __str__(self):
        return f"{self.result} = load {self.address}"


@dataclass(frozen=True)
class Store(Instruction):
    value: Value
    address: Value

    def __str__(self):
        return f"store {self.value}, {self.address}"


@dataclass(frozen=True)
class Fence(Instruction):
    def __str__(self):
        return f"fence"


@dataclass(frozen=True)
class CmpXchg(Instruction):
    address: Value
    check_value: Value
    new_value: Value

    def __str__(self):
        return f"{self.result} = cmpxchg {self.address}, {self.check_value}, {self.new_value}"


@dataclass(frozen=True)
class AtomicRmw(Instruction):
    op: str
    address: Value
    operand: Value

    def __str__(self):
        return f"{self.result} = atomicrmw {self.op} {self.address}, {self.operand}"


@dataclass(frozen=True)
class GetElementPtr(Instruction):
    dest_ty: Type
    source_ty: Type
    base_addr: Value
    indices: list[Value]

    def __str__(self):
        return f"{self.result} = getelementptr {self.result.ty}, {self.base_addr}, " + (
            f"{','.join(map(str, self.indices))}"
        )


@dataclass(frozen=True)
class Conversion(Instruction):
    value: Value
    # source type is type of the value
    # dest type is type of the result

    def __str__(self):
        return f"{self.result} = {self.opcode} {self.value} to {self.result.ty}"


@dataclass(frozen=True)
class ICmp(Instruction):
    cond: str
    arg0: Value
    arg1: Value

    def __str__(self):
        return f"{self.result} = icmp {self.cond} {self.arg0}, {self.arg1}"


@dataclass(frozen=True)
class FCmp(Instruction):
    cond: str
    arg0: Value
    arg1: Value

    def __str__(self):
        return f"{self.result} = fcmp {self.cond} {self.arg0}, {self.arg1}"


@dataclass(frozen=True)
class Phi(Instruction):
    vals: list[tuple[Value, Value]]  # (val, label)

    def __str__(self):
        return f"{self.result} = phi {', '.join(f'{val}, {label}' for val, label in self.vals)}"


@dataclass(frozen=True)
class Select(Instruction):
    cond: Value
    true_value: Value
    false_value: Value

    def __str__(self):
        return f"{self.result} = {self.cond}, {self.true_value}, {self.false_value}"


@dataclass(frozen=True)
class Freeze(Instruction):
    value: Value

    def __str__(self):
        return f"{self.result} = freeze {self.value}"


@dataclass(frozen=True)
class Call(CallInstr):
    func: Value
    args: list[Value]

    def __str__(self):
        return f"{self.result} = call {self.func}({', '.join(map(str, self.args))})"


@dataclass(frozen=True)
class VaArg(Instruction):
    value: Value

    def __str__(self):
        return f"{self.result} = va_arg {self.value}"


@dataclass(frozen=True)
class LangingPad(Instruction):
    is_cleanup: bool
    is_catchs: list[bool]
    clauses: list[Value]

    def __str__(self):
        clauses = " ".join(
            "catch " if is_catch else "filter " + str(clause)
            for is_catch, clause in zip(self.is_catchs, self.clauses)
        )
        return f"{self.result} = landingpad {clauses}"


@dataclass(frozen=True)
class CatchPad(Instruction):
    catchswith: Value
    args: list[Value]

    def __str__(self):
        return f"{self.result} = catchpad within {self.catchswith} [{' '.join(map(str, self.args))}]"


@dataclass(frozen=True)
class CleanupPad(Instruction):
    parent: Value
    args: list[Value]

    def __str__(self):
        return f"{self.result} = cleanuppad within {self.parent} [{' '.join(map(str, self.args))}]"


_constructors = [
    # branch
    # 1
    (
        Ret,
        lambda operands, additional, callattrs: (
            operands if len(operands) != 0 else (None,)
        ),
    ),
    # 2
    (
        Br,
        lambda operands, additional, callattrs: (
            (None, *operands, None) if (len(operands) == 1) else operands
        ),
    ),
    # 3
    (
        Switch,
        lambda operands, additional, callattrs: (
            operands[0],
            operands[1],
            list(zip(operands[2::2], operands[3::2])),
        ),
    ),
    # 4
    (
        IndirectBr,
        lambda operands, additional, callattrs: (operands[0], operands[1:]),
    ),
    # 5
    (
        Invoke,
        lambda operands, additional, callattrs: (
            callattrs,
            operands[-1],
            operands[:-3],
            operands[-3],
            operands[-2],
        ),
    ),
    # 6
    (
        Resume,
        lambda operands, additional, callattrs: operands,
    ),
    # 7
    (Unreacheble, lambda operands, additional, callattrs: []),
    # 8
    (CleanupRet, lambda operands, additional, callattrs: operands),
    # 9
    (
        CatchRet,
        lambda operands, additional, callattrs: operands,
    ),
    # 10
    (
        CatchSwitch,
        lambda operands, additional, callattrs: (
            (operands[0], operands[2:], operands[1])
            if additional[0]
            else (operands[0], operands[1:], None)
        ),
    ),
    # 11
    (
        CallBr,
        lambda operands, additional, callattrs: (
            callattrs,
            operands[-1],
            operands[: -additional[0] - 2],
            operands[-additional[0] - 2],
            operands[-additional[0] - 1 : -1],
        ),
    ),
    # unary, 12
    (UnaryOp, lambda operands, additional, callattrs: operands),
    # binary, 13
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    # bitwise, 25
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    (BinOp, lambda operands, additional, callattrs: operands),
    # memory, 31
    (Alloca, lambda operands, additional, callattrs: (*operands, additional[0])),
    (Load, lambda operands, additional, callattrs: operands),
    (Store, lambda operands, additional, callattrs: operands),
    (
        GetElementPtr,
        lambda operands, additional, callattrs: (
            additional[0],
            additional[1],
            operands[0],
            operands[1:],
        ),
    ),
    (Fence, lambda operands, additional, callattrs: []),
    (CmpXchg, lambda operands, additional, callattrs: operands),
    (AtomicRmw, lambda operands, additional, callattrs: (additional[0], *operands)),
    # conversion, 38
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    (Conversion, lambda operands, additional, callattrs: operands),
    # pads, 51
    (
        CleanupPad,
        lambda operands, additional, callattrs: (operands[-1], operands[:-1]),
    ),
    (
        CatchPad,
        lambda operands, additional, callattrs: (operands[-1], operands[:-1]),
    ),
    # other, 53
    (ICmp, lambda operands, additional, callattrs: (additional[0], *operands)),
    (FCmp, lambda operands, additional, callattrs: (additional[0], *operands)),
    (
        Phi,
        lambda operands, additional, callattrs: (list(zip(operands, additional[0])),),
    ),
    (
        Call,
        lambda operands, additional, callattrs: (
            callattrs,
            operands[-1],
            operands[:-1],
        ),
    ),
    (Select, lambda operands, additional, callattrs: operands),
    # user ops, 58
    (UserInstructionContainer, lambda operands, additional, callattrs: (operands,)),
    (UserInstructionContainer, lambda operands, additional, callattrs: (operands,)),
    # 60
    (VaArg, lambda operands, additional, callattrs: operands),
    # vector, 61
    (ExtractElement, lambda operands, additional, callattrs: operands),
    (InsertElement, lambda operands, additional, callattrs: operands),
    (ShuffleVector, lambda operands, additional, callattrs: operands),
    # aggregate, 64
    (ExtractValue, lambda operands, additional, callattrs: (*operands, additional[0])),
    (InsertValue, lambda operands, additional, callattrs: (*operands, additional[0])),
    (
        LangingPad,
        lambda operands, additional, callattrs: (
            additional[0],
            additional[1],
            operands,
        ),
    ),
    (Freeze, lambda operands, additional, callattrs: operands),
]


def _create_instruction(
    opcode: int,
    opcode_name: str,
    operands: list[Value],
    additional: tuple,
    attributes: Any,
    call_attributes: Any,
    value: Value,
):
    constructor, make_params = _constructors[opcode - 1]
    params = make_params(operands, additional, call_attributes)
    return constructor(attributes, value, opcode_name, *params)
