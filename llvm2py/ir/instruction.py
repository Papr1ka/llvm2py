from typing import Any, Callable, Iterable, NamedTuple, Literal, Union
from .type import Type
from .value import Value
from .support import attrs_to_dict, attrs_list_to_dict
from .enum import CallingConv, Ordering, Attrs


# fmt: off
class Ret(NamedTuple):
    """
    
    `Ret instruction <https://llvm.org/docs/LangRef.html#ret-instruction>`_.
    
    The ‘ret’ instruction is used to return control flow (and optionally a value)
    from a function back to the caller.

    There are two forms of the ‘ret’ instruction:
    one that returns a value and then causes control flow,
    and one that just causes control flow to occur.

    :param value: A return value.
    :type value: Value | None
    
    Conversation::
    
        ret <type> <value>       ; Return a value from a non-void function
        Ret(
            Value(value, type),
        )
        
        ret void                 ; Return from void function
        Ret(None)
    """

    value: Value | None = None


class Br(NamedTuple):
    """
    `Branch instruction <https://llvm.org/docs/LangRef.html#br-instruction>`_.
    
    The ‘br’ instruction is used to cause control flow to transfer to a different basic block
    in the current function.
    There are two forms of this instruction, corresponding to a conditional branch
    and an unconditional branch.

    :param cond: A condition.
    :type cond: Value
    :param label_false: If cond is False, control flows to the label_false.
    :type label_false: Value
    :param label_true: If cond is True, control flows to the label_true.
    :type label_true: Value | None

    Conversation::
    
        br i1 <cond>, label <iftrue>, label <iffalse>
        Br(
            Value(cond, IntegerType(1)),
            Value(iffalse, LabelType()),
            Value(iftrue, LabelType()),
        )
        
        br label <dest>          ; Unconditional branch
        Br(
            None,
            Value(dest, LabelType()),
            None
        )
    """

    cond: Value | None
    label_false: Value
    label_true: Value | None


class Switch(NamedTuple):
    """
    `Switch instruction <https://llvm.org/docs/LangRef.html#switch-instruction>`_.
    
    The ‘switch’ instruction is used to transfer control flow to one of several different places.
    It is a generalization of the ‘br’ instruction, allowing
    a branch to occur to one of many possible destinations.

    :param cond: A comparison value.
    :type cond: Value
    :param label_default: A default destination label.
    :type label_default: Value
    :param cases: A list of pairs of comparison values and labels.
    :type cases: list[tuple[Value, Value]]

    Conversation::
    
        switch <intty> <value>, label <defaultdest> [ <intty> <val>, label <dest> ... ]
        Switch(
            Value(value, intty),
            Value(defaultdest, LabelType()),
            [
                (Value(val, intty), Value(dest, LabelType())),
                ...
            ]
        )
    """
    
    cond: Value
    label_default: Value
    cases: list[tuple[Value, Value]]  # [(cond, label)]

class IndirectBr(NamedTuple):
    """
    `Indirect branch instruction <https://llvm.org/docs/LangRef.html#indirectbr-instruction>`_.
    
    The ‘indirectbr’ instruction implements an indirect branch to a label
    within the current function, whose address is specified by “address”.
    Address must be derived from a blockaddress constant.

    :param addr: The address of the label to jump to.
    :type addr: Value
    :param possible_dests: A list, indicating the full set of possible destinations that the address may point to.
    :type possible_dests: list[Value]

    Conversation::
    
        indirectbr ptr <address>, [ label <dest1>, label <dest2>, ... ]
        IndirectBr(
            Value(address, PtrType(...)),
            [
                Value(dest1, LabelType()),
                Value(dest2, LabelType()),
                ...
            ]
        )
    """
    
    addr: Value
    possible_dests: list[Value]


class Invoke(NamedTuple):
    """
    `Invoke instruction <https://llvm.org/docs/LangRef.html#invoke-instruction>`_.
        
    The ‘invoke’ instruction causes control to transfer to a specified function,
    with the possibility of control flow transfer to either the ‘normal’ label
    or the ‘exception’ label. If the callee function returns with the “ret” instruction,
    control flow will return to the “normal” label. If the callee (or any indirect callees)
    returns via the “resume” instruction or other exception handling mechanism,
    control is interrupted and continued at the dynamically nearest “exception” label.

    The ‘exception’ label is a landing pad for the exception.
    As such, ‘exception’ label is required to have the “landingpad” instruction,
    which contains the information about the behavior of the program
    after unwinding happens, as its first non-PHI instruction.
    The restrictions on the “landingpad” instruction’s tightly couples
    it to the “invoke” instruction, so that the important information
    contained within the “landingpad” instruction can’t be lost through normal code motion.

    :param result: A returned value.
    :type result: Value
    :param callee: The function to be invoked, pointer or function name.
    :type callee: Value
    :param args: An argument list.
    :type args: list[Value]
    :param label_ok: The label reached when the called function executes a ‘ret’ instruction.
    :type label_ok: Value
    :param label_err: The label reached when a callee returns via the resume instruction
        or other exception handling mechanism.
    :type label_err: Value
    :param calling_conv: The calling convention that should be used in a call.
    :type calling_conv: CallingConv
    :param call_attrs: A list containing all call-related attributes.
    :type call_attrs: list[Attrs]

    Conversation::
    
        <result> = invoke [cconv] [ret attrs] [addrspace(<num>)] <ty>|<fnty> <fnptrval>(<function args>) [fn attrs]
              [operand bundles] to label <normal label> unwind label <exception label>
        Invoke(
            Value(result, Type),
            Value(fnptrval, FunctionType | Type),
            [
                Value(arg0, Type),
                Value(arg1, Type),
                ...
            ],
            Value(label_ok, LabelType()),
            Value(label_err, LabelType()),
            cconv,
            [call_attrs]
        )
    """
    
    result: Value
    callee: Value
    args: list[Value]
    label_ok: Value
    label_err: Value
    calling_conv: CallingConv
    call_attrs: list[Attrs]


class Resume(NamedTuple):
    """
    `Resume instruction <https://llvm.org/docs/LangRef.html#resume-instruction>`_.
        
    The ‘resume’ instruction is a terminator instruction that has no successors.

    :param val: An exception whose propagation to resume.
    :type val: Value

    Conversation::
    
        resume <type> <value>
        Resume(
            Value(value, type),
        )
    """
    
    val: Value


class CallBr(NamedTuple):
    """
    `CallBr instruction <https://llvm.org/docs/LangRef.html#callbr-instruction>`_.
        
    The ‘callbr’ instruction causes control to transfer to a specified function,
    with the possibility of control flow transfer to either the ‘fallthrough’ label
    or one of the ‘indirect’ labels.
    
    This instruction should only be used to implement the “goto” feature
    of gcc style inline assembly. Any other usage is an error in the IR verifier.
    
    Note that in order to support outputs along indirect edges,
    LLVM may need to split critical edges, which may require synthesizing
    a replacement block for the indirect labels.
    Therefore, the address of a label as seen by another callbr instruction,
    or for a blockaddress constant, may not be equal to the address provided
    for the same block to this instruction’s indirect labels operand.
    The assembly code may only transfer control to addresses provided
    via this instruction’s indirect labels.

    :param result: A return value.
    :type result: Value
    :param callee: The function to be invoked, **inline asm** or pointer.
    :type callee: Value
    :param args: An argument list.
    :type args: list[Value]
    :param fallthrough_label: The label reached when the inline assembly’s execution exits the bottom.
    :type fallthrough_label: Value
    :param indirect_labels: The labels reached when a callee transfers control to
        a location other than the ‘fallthrough label’.
        The label constraints refer to these destinations.
    :type indirect_labels: list[Value]
    
    :param calling_conv: The calling convention that should be used in a call.
    :type calling_conv: CallingConv
    :param call_attrs: A list containing all call-related attributes.
    :type call_attrs: list[Attrs]

    Conversation::
    
        <result> = callbr [cconv] [ret attrs] [addrspace(<num>)] <ty>|<fnty> <fnptrval>(<function args>) [fn attrs]
              [operand bundles] to label <fallthrough label> [indirect labels]
        CallBr(
            Value(result, Type),
            Value(fnptrval, FunctionType | Type),
            [
                Value(arg0, Type),
                Value(arg1, Type),
                ...
            ],
            Value(fallthrough label, LabelType()),
            [
                Value(label0, LabelType()),
                Value(label1, LabelType()),
                ...
            ]
            cconv,
            [call_attrs],
            attrs
        )
    
    .. note::
        addrspace can be retrieved from a function global object
    """
    
    result: Value
    callee: Value
    args: list[Value]
    fallthrough_label: Value
    indirect_labels: list[Value]
    calling_conv: CallingConv
    call_attrs: list[Attrs]


class CatchSwitch(NamedTuple):
    """
    `CatchSwitch instruction <https://llvm.org/docs/LangRef.html#catchswitch-instruction>`_.
    
    The ‘catchswitch’ instruction is used by LLVM’s exception handling system
    to describe the set of possible catch handlers that may be executed
    by the EH personality routine.

    :param result: A result value.
    :type result: Value
    :param parent: The token of the funclet that contains the catchswitch instruction.
        If the catchswitch is not inside a funclet, this operand may be the token none.
    :type parent: Value
    :param handler_labels: A list of successor blocks that each begin with a catchpad instruction.
    :type handler_labels: list[Value]
    :param label_default: The label of another basic block beginning with either a cleanuppad or catchswitch instruction.
    :type label_default: Value | None

    Conversation::
    
        <resultval> = catchswitch within <parent> [ label <handler1>, label <handler2>, ... ] unwind to caller
        CatchSwitch(
            Value(resultval, TokenType()),
            Value(parent, Type),
            [
                Value(handler1, LabelType()),
                Value(handler2, LabelType()),
                ...
            ]
        )
        
        <resultval> = catchswitch within <parent> [ label <handler1>, label <handler2>, ... ] unwind label <default>
        CatchSwitch(
            Value(resultval, Type),
            Value(parent, Type),
            [
                Value(handler1, LabelType()),
                Value(handler2, LabelType()),
                ...
            ]
            Value(default, LabelType())
        )
    """
    
    result: Value
    parent: Value
    handler_labels: list[Value]
    label_default: Value | None = None


class CatchRet(NamedTuple):
    """
    `CatchRet instruction <https://llvm.org/docs/LangRef.html#catchret-instruction>`_.
    
    The ‘catchret’ instruction is a terminator instruction that has a single successor.

    :param catch: A token indicating which catchpad it exits.
    :type catch: Value
    :param succ_label: A label to which control will be transferred.
    :type succ_label: Value

    Conversation::
    
        catchret from <token> to label <normal>
        CatchRet(
            Value(token, TokenType()),
            Value(normal, LabelType())
        )
    """
    
    catch: Value
    succ_label: Value


class CleanupRet(NamedTuple):
    """
    `CleanupRet instruction <https://llvm.org/docs/LangRef.html#cleanupret-instruction>`_.
    
    The ‘cleanupret’ instruction is a terminator instruction that has an optional successor.

    :param cleanup: A token indicating which cleanuppad it exits, must be a cleanuppad.
    :type cleanup: Value
    :param succ_label: A successor, the label of another basic block beginning with either a cleanuppad or catchswitch instruction.
    :type succ_label: Value | None

    Conversation::
    
        cleanupret from <value> unwind label <continue>
        CleanupRet(
            Value(value, TokenType()),
            Value(continue, LabelType())
        )
        
        cleanupret from <value> unwind to caller
        CleanupRet(
            Value(value, TokenType())
        )
    """
    cleanup: Value
    succ_label: Value | None = None


class Unreacheble:
    """
    `Unreacheble instruction <https://llvm.org/docs/LangRef.html#unreachable-instruction>`_.
    
    The ‘unreachable’ instruction has no defined semantics.
    This instruction is used to inform the optimizer that a particular portion
    of the code is not reachable. This can be used to indicate that the code
    after a no-return function cannot be reached, and other facts.

    Conversation::
    
        unreachable
        Unreacheble()
    """
    pass


class UnaryOp(NamedTuple):
    """
    `Unary operations <https://llvm.org/docs/LangRef.html#unary-operations>`_.
    
    Unary operators require a single operand, execute an operation on it, and produce
    a single value. The operand might represent multiple data, as is the case
    with the vector data type. The result value has the same type as its operand.
    
    This class generalizes all unary operations

    :param opcode: An instuction opcode, one of {'fneg'}.
    :type opcode: str
    :param result: The produced value.
    :type result: Value
    :param operand: An operand.
    :type operand: Value
    :param fast_math_flags: The set of fast math flags.
    :type fast_math_flags: frozenset[str]

    Conversation::
    
        <result> = fneg [fast-math flags]* <ty> <op1>   ; yields ty:result
        UnaryOp(
            'fneg'
            Value(result, ty),
            Value(op1, ty),
            {*fast-math flags}
        )
    """
    
    opcode: str
    result: Value
    operand: Value
    fast_math_flags: frozenset[str] = frozenset()


class BinOp(NamedTuple):
    """
    `BinOp instruction <https://llvm.org/docs/LangRef.html#binary-operations>`_.
    
    Binary operators are used to do most of the computation in a program.
    They require two operands of the same type, execute an operation on them,
    and produce a single value. The operands might represent multiple data,
    as is the case with the vector data type. The result value has the same type
    as its operands.
    
    This class generalizes all binary operations.

    :param opcode: An instuction opcode, one of {
        'add', 'fadd', 'sub', 'fsub', 'mul',
        'fmul', 'udiv', 'sdiv', 'fdiv', 'urem',
        'srem', 'frem', 'shl', 'lshr', 'ashr',
        'and', 'or', 'xor'
        }.
    :type opcode: str
    :param result: The produced value.
    :type result: Value
    :param fst_operand: The first operand.
    :type fst_operand: Value
    :param snd_operand: The second operand.
    :type snd_operand: Value
    :param fast_math_flags: The set of fast math flags.
    :type fast_math_flags: frozenset[str]
    :param is_nuw: If True, the instruction has a "nuw" flag.
    :type is_nuw: bool
    :param is_nsw: If True, the instruction has a "nsw" flag.
    :type is_nsw: bool
    :param is_exact: If True, the instruction has a "exact" flag.
    :type is_exact: bool
    :param is_disjoint: If True, the instruction has a "disjoint" flag.
    :type is_disjoint: bool

    Conversation::
    
        <result> = <opcode> [fast-math flags]* [nuw] [nsw] [exact] [disjoint] <ty> <op1>, <op2>  ; yields ty:result
        BinOp(
            opcode
            Value(result, ty),
            Value(op1, ty),
            Value(op2, ty),
            attrs
        )
    """
    
    opcode: str
    result: Value
    fst_operand: Value
    snd_operand: Value
    fast_math_flags: frozenset[str] = frozenset()
    is_nuw: bool = False
    is_nsw: bool = False
    is_exact: bool = False
    is_disjoint: bool = False


class ExtractElement(NamedTuple):
    """
    `ExtractElement instruction <https://llvm.org/docs/LangRef.html#extractelement-instruction>`_.
    
    The ‘extractelement’ instruction extracts a single scalar element
    from a vector at a specified index.

    :param result: A scalar of the same type as the element type of vector.
    :type result: Value
    :param vector: A value of vector type.
    :type vector: Value
    :param index: An index indicating the position from which to extract the element.
    :type index: Value

    Conversation::
    
        <result> = extractelement <n x <ty>> <val>, <ty2> <idx>  ; yields <ty>
        ExtractElement(
            Value(result, ty),
            Value(val, VectorType(n, ty)),
            Value(idx, ty2),
        )
        
        <result> = extractelement <vscale x n x <ty>> <val>, <ty2> <idx> ; yields <ty>
        ExtractElement(
            Value(result, ty)),
            Value(val, VectorType(n, ty, True)),
            Value(idx, ty2),
        )
    """
    
    result: Value
    vector: Value
    index: Value


class InsertElement(NamedTuple):
    """
    `InsertElement instruction <https://llvm.org/docs/LangRef.html#insertelement-instruction>`_.
    
    The ‘insertelement’ instruction inserts a scalar element into a vector at a specified index.

    :param result: A vector of the same type as val.
    :type result: Value
    :param vector: A value of vector type.
    :type vector: Value
    :param elem: A scalar value whose type must equal the element type of the first operand.
    :type elem: Value
    :param index: An index indicating the position at which to insert the value.
    :type index: Value

    Conversation::
    
        <result> = insertelement <n x <ty>> <val>, <ty> <elt>, <ty2> <idx>    ; yields <n x <ty>>
        InsertElement(
            Value(result, VectorType(n, ty)),
            Value(val, VectorType(n, ty)),
            Value(elt, ty),
            Value(idx, ty2),
        )
        
        <result> = insertelement <vscale x n x <ty>> <val>, <ty> <elt>, <ty2> <idx> ; yields <vscale x n x <ty>>
        InsertElement(
            Value(result, VectorType(n, ty, True)),
            Value(val, VectorType(n, ty, True)),
            Value(elt, ty),
            Value(idx, ty2),
        )
    """
    result: Value
    vector: Value
    elem: Value
    index: Value


class ShuffleVector(NamedTuple):
    """
    `ShuffleVector instruction <https://llvm.org/docs/LangRef.html#shufflevector-instruction>`_.
    
    The ‘shufflevector’ instruction constructs a permutation of elements
    from two input vectors, returning a vector with the same element
    type as the input and length that is the same as the shuffle mask.

    :param result: A vector whose length is the same as the shuffle mask
        and whose element type is the same as the element type of the first two operands.
    :type result: Value
    :param fst_vector: A value of vector type.
    :type fst_vector: Value
    :param snd_vector: A value of vector type with the same type as fst_vector.
    :type snd_vector: Value
    :param mask_vector: A shuffle mask vector constant whose element type is i32,
        if the value of the mask_vector element is -1,
        the result element must have the poison or undef value.
        A "zeroinitializer" represented as an array of zeros.
    :type mask_vector: list[int]

    Conversation::
    
        <result> = shufflevector <n x <ty>> <v1>, <n x <ty>> <v2>, <m x i32> <mask>    ; yields <m x <ty>>
        ShuffleVector(
            Value(result, VectorType(m, ty)),
            Value(v1, VectorType(n, ty)),
            Value(v2, VectorType(n, ty)),
            [mask_0, ..., mask_(m-1)],
        )
        
        <result> = shufflevector <vscale x n x <ty>> <v1>, <vscale x n x <ty>> v2, <vscale x m x i32> <mask>  ; yields <vscale x m x <ty>>
        ShuffleVector(
            Value(result, VectorType(m, ty, True)),
            Value(v1, VectorType(n, ty, True)),
            Value(v2, VectorType(n, ty, True)),
            [mask_0, ..., mask_(m-1)],
        )
    """
    result: Value
    fst_vector: Value
    snd_vector: Value
    mask_vector: list[int]


class ExtractValue(NamedTuple):
    """
    `ExtractValue instruction <https://llvm.org/docs/LangRef.html#extractvalue-instruction>`_.
    
    The ‘extractvalue’ instruction extracts the value of a member field from an aggregate value.

    :param result: The value at the position in the aggregate specified by the index operands.
    :type result: Value
    :param aggregate: A value of struct or array type.
    :type aggregate: Value
    :param indices: A list of constant indices to specify which value
        to extract in a similar manner as indices in a ‘getelementptr’ instruction.
    :type indices: list[int]
    
    Conversation::
    
        <result> = extractvalue <aggregate type> <val>, <idx>{, <idx>}*
        ExtractValue(
            Value(result, Type),
            Value(val, aggregate type),
            [idx0, idx1, ...],
        )
    """
    
    result: Value
    aggregate: Value
    indices: list[int]


class InsertValue(NamedTuple):
    """
    `InsertValue instruction <https://llvm.org/docs/LangRef.html#insertvalue-instruction>`_.
    
    The ‘insertvalue’ instruction inserts a value into a member field in an aggregate value.

    :param result: A value of the same type as aggregate.
        Its value is that of aggregate except that the value
        at the position specified by the indices is that of elem.
    :type result: Value
    :param aggregate: A value of struct or array type.
    :type aggregate: Value
    :param elem: A value to insert.
    :type elem: Value
    :param indices: A list of constant indices indicating the position at which
        to insert the value in a similar manner as indices in a ‘extractvalue’ instruction.
    :type indices: list[int]
    
    Conversation::
    
        <result> = insertvalue <aggregate type> <val>, <ty> <elt>, <idx>{, <idx>}*    ; yields <aggregate type>
        InsertValue(
            Value(result, aggregate type),
            Value(val, aggregate type),
            Value(elt, ty)
            [idx0, idx1, ...],
        )
    """
    result: Value
    aggregate: Value
    elem: Value
    indices: list[int]


class Alloca(NamedTuple):
    """
    `Alloca instruction <https://llvm.org/docs/LangRef.html#alloca-instruction>`_.
    
    The ‘alloca’ instruction allocates memory on the stack frame of the
    currently executing function, to be automatically released when
    this function returns to its caller.

    :param result: A pointer to uninitialized allocated memory.
    :type result: Value
    :param allocated_ty: The type to allocate.
    :type allocated_ty: Type
    :param num_elements: The number of elements to allocate.
    :type num_elements: Value
    :param align: If specified, the value result of the allocation is guaranteed
        to be aligned to at least that boundary.
    :type align: int
    :param is_inalloca: If True, the instruction has a "inalloca" flag.
    :type is_inalloca: bool
    
    Conversation::
    
        <result> = alloca [inalloca] <type> [, <ty> <NumElements>] [, align <alignment>] [, addrspace(<num>)]     ; yields type addrspace(num)*:result
        Alloca(
            Value(result, PtrType(num)),
            type
            Value(NumElements, ty),
            alignment,
            inalloca?
        )
    """
    result: Value
    allocated_ty: Type
    num_elements: Value
    align: int = 0
    is_inalloca: bool = False


class Load(NamedTuple):
    """
    `Load instruction <https://llvm.org/docs/LangRef.html#load-instruction>`_.
    
    The ‘load’ instruction is used to read from memory.

    :param result: The loaded value.
    :type result: Value
    :param address: The memory address from which to load.
    :type address: Value
    :param align: The alignment of the operation (that is, the alignment of the memory address).
    :type align: int
    :param is_volatile: If True, the instruction has a "volatile" flag.
    :type is_volatile: bool
    :param is_atomic: If True, the instruction is atomic.
    :type is_atomic: bool
    :param ordering: https://llvm.org/docs/LangRef.html#ordering
    :type ordering: Ordering
    :param syncscope: https://llvm.org/docs/LangRef.html#syncscope
    :type syncscope: int | None
    
    Conversation::
    
        <result> = load [volatile] <ty>, ptr <pointer>[, align <alignment>]
        Load(
            Value(result, ty),
            Value(pointer, ptr),
            alignment,
            volatile?
        )
    
        <result> = load atomic [volatile] <ty>, ptr <pointer> [syncscope("<target-scope>")] <ordering>, align <alignment>
        Load(
            Value(result, ty),
            Value(pointer, ptr),
            alignment,
            volatile?
            True
            ordering
            target-scope
        )
    """
    result: Value
    address: Value
    align: int = 0
    is_volatile: bool = False
    is_atomic: bool = False
    ordering: Ordering = Ordering.NotAtomic
    syncscope: int | None = None


class Store(NamedTuple):
    """
    `Store instruction <https://llvm.org/docs/LangRef.html#store-instruction>`_.
    
    The ‘store’ instruction is used to write to memory.
    
    :param value: The value to store.
    :type value: Value
    :param address: An address at which to store value.
    :type address: Value
    :param align: The alignment of the operation (that is, the alignment of the memory address).
    :type align: int
    :param is_volatile: If True, the instruction has a "volatile" flag.
    :type is_volatile: bool
    :param is_atomic: If True, the instruction is atomic.
    :type is_atomic: bool
    :param ordering: https://llvm.org/docs/LangRef.html#ordering
    :type ordering: Ordering
    :param syncscope: https://llvm.org/docs/LangRef.html#syncscope
    :type syncscope: int | None
    
    Conversation::
    
        store [volatile] <ty> <value>, ptr <pointer>[, align <alignment>] yields void
        Store(
            Value(value, ty),
            Value(pointer, ptr),
            alignment,
            volatile?
        )
    
        store atomic [volatile] <ty> <value>, ptr <pointer> [syncscope("<target-scope>")] <ordering>, align <alignment> ; yields void
        Store(
            Value(value, ty),
            Value(pointer, ptr),
            alignment,
            volatile?
            True
            ordering
            target-scope
        )
    """
    value: Value
    address: Value
    align: int = 0
    is_volatile: bool = False
    is_atomic: bool = False
    ordering: Ordering = Ordering.NotAtomic
    syncscope: int | None = None


class Fence(NamedTuple):
    """
    `Fence instruction <https://llvm.org/docs/LangRef.html#fence-instruction>`_.
    
    The ‘fence’ instruction is used to introduce happens-before edges between operations.
    
    :param ordering: https://llvm.org/docs/LangRef.html#ordering
    :type ordering: Ordering
    :param syncscope: https://llvm.org/docs/LangRef.html#syncscope
    :type syncscope: int | None
    
    Conversation::
    
        fence [syncscope("<target-scope>")] <ordering>  ; yields void
        Fence(
            ordering,
            target-scope
        )
    """
    ordering: Ordering
    syncscope: int | None = None


class CmpXchg(NamedTuple):
    """
    `CmpXchg instruction <https://llvm.org/docs/LangRef.html#cmpxchg-instruction>`_.
    
    The ‘cmpxchg’ instruction is used to atomically modify memory.
    It loads a value in memory and compares it to a given value.
    If they are equal, it tries to store a new value into the memory.
    
    :param result: A struct with the original value at the location
        and a flag indicating success (true) or failure (false).
    :type result: Value
    :param address: An address to operate on.
    :type address: Value
    :param compare_value: A value to compare to the value currently be at the address.
    :type compare_value: Value
    :param new_value: A new value to place at the address if the compared values are equal.
    :type new_value: Value
    :param ordering_ok: https://llvm.org/docs/LangRef.html#ordering
    :type ordering_ok: Ordering
    :param ordering_err: https://llvm.org/docs/LangRef.html#ordering
    :type ordering_err: Ordering
    :param align: An alignment.
    :type align: int
    :param is_weak: If True, the instruction has a "weak" flag.
    :type is_weak: bool
    :param is_volatile: If True, the instruction has a "volatile" flag.
    :type is_volatile: bool
    :param syncscope: https://llvm.org/docs/LangRef.html#syncscope
    :type syncscope: int | None
    
    Conversation::
    
        <result> = cmpxchg [weak] [volatile] ptr <pointer>, <ty> <cmp>, <ty> <new> [syncscope("<target-scope>")] <success ordering> <failure ordering>[, align <alignment>] ; yields  { ty, i1 }
        CmpXchg(
            Value(result, StructureType(elem_tys=[ty, IntegerType(1)])),
            Value(pointer, ptr),
            Value(cmp, ty),
            Value(new, ty),
            success ordering,
            failure ordering,
            alignment,
            weak?
            volatile?
            target-scope
        )
    """
    result: Value
    address: Value
    compare_value: Value
    new_value: Value
    ordering_ok: Ordering
    ordering_err: Ordering
    align: int = 0
    is_weak: bool = False
    is_volatile: bool = False
    syncscope: int | None = None


class AtomicRmw(NamedTuple):
    """
    `AtomicRmw instruction <https://llvm.org/docs/LangRef.html#atomicrmw-instruction>`_.
    
    The ‘atomicrmw’ instruction is used to atomically modify memory.
    
    :param op: An operation to apply, one of {
        'xchg', 'add', 'sub', 'and', 'nand',
        'or', 'xor', 'max', 'min', 'umax',
        'umin', 'fadd', 'fsub', 'fmax', 'fmin',
        'uinc_wrap', 'udec_wrap', 'usub_cond', 'usub_sat'
        }.
    :type op: str
    :param result: The original value at the location.
    :type result: Value
    :param address: An address whose value to modify.
    :type address: Value
    :param operand: An argument to the operation.
    :type operand: Value
    :param ordering: https://llvm.org/docs/LangRef.html#ordering
    :type ordering: Ordering
    :param align: An alignment.
    :type align: int
    :param is_volatile: If True, the instruction has a "volatile" flag.
    :type is_volatile: bool
    :param syncscope: https://llvm.org/docs/LangRef.html#syncscope
    :type syncscope: int | None
    
    Conversation::
    
        <result> = atomicrmw [volatile] <operation> ptr <pointer>, <ty> <value> [syncscope("<target-scope>")] <ordering>[, align <alignment>]  ; yields ty
        AtomicRmw(
            operation,
            Value(result, ty),
            Value(pointer, ptr),
            Value(value, ty),
            ordering,
            alignment,
            volatile?
            target-scope
        )
    """
    op: str
    result: Value
    address: Value
    operand: Value
    ordering: Ordering
    align: int = 0
    is_volatile: bool = False
    syncscope: int | None = None


class GetElementPtr(NamedTuple):
    """
    `GetElementPtr instruction <https://llvm.org/docs/LangRef.html#getelementptr-instruction>`_.
    
    The ‘getelementptr’ instruction is used to get the address
    of a subelement of an aggregate data structure.
    It performs address calculation only and does not access memory.
    The instruction can also be used to calculate a vector of such addresses.
    
    :param result: The resulting address.
    :type result: Value
    :param source_ty: A type used as the basis for the calculations.
    :type source_ty: Type
    :param base_addr: A pointer, or vector of pointers, the base address to start with.
    :type base_addr: Value
    :param indices: A list indicationg which of the elements of the aggregate object are indexed.
    :type indices: list[Value]
    :param dest_ty: The type pointed to by the received address.
    :type dest_ty: Type
    :param is_inbounds: If True, the instruction has a "inbounds" flag.
    :type is_inbounds: str | None
    
    Conversation::
    
        <result> = getelementptr [inbounds] <ty>, ptr <ptrval>{, <ty> <idx>}*
        GetElementPtr(
            Value(result, PtrType(...)),
            ty,
            Value(ptrval, ptr),
            [
                Value(idx0, ty),
                Value(idx1, ty),
                ...
            ]
        )
    """
    result: Value
    source_ty: Type
    base_addr: Value
    indices: list[Value]
    dest_ty: Type | None = None
    is_inbounds: bool = False
    

class Conversion(NamedTuple):
    """
    `Conversion operations <https://llvm.org/docs/LangRef.html#conversion-operations>`_.
    
    These instructions are the conversion instructions (casting)
    which all take a single operand and a type.
    They perform various bit conversions on the operand.
    
    This class generalizes all conversion operations.

    :param opcode: An instuction opcode, one of {
        'trunc', 'zext', 'sext', 'fptrunc', 'fpext',
        'fptoui', 'fptosi', 'uitofp', 'sitofp', 'ptrtoint',
        'inttoptr', 'bitcast', 'addrspacecast'
        }.
    :type opcode: str
    :param result: The converted value.
    :type result: Value
    :param value: A value to convert.
    :type value: Value
    :param fast_math_flags: A set of fast math flags.
    :type fast_math_flags: frozenset[str]
    :param is_nuw: If True, the instruction has a "nuw" flag.
    :type is_nuw: bool
    :param is_nsw: If True, the instruction has a "nsw" flag.
    :type is_nsw: bool
    
    Conversation::
    
        <result> = opcode [fast-math flags]* [nuw] [nsw] <ty> <value> to <ty2>     ; yields ty2
        Conversion(
            opcode,
            Value(result, ty2),
            Value(value, ty),
            {*fast-math flags},
            nuw?
            nsw?
        )
    """
    
    opcode: str
    result: Value
    value: Value
    fast_math_flags: frozenset[str] = frozenset()
    is_nuw: bool = False
    is_nsw: bool = False


class ICmp(NamedTuple):
    """
    `ICmp instruction <https://llvm.org/docs/LangRef.html#icmp-instruction>`_.
    
    The ‘icmp’ instruction returns a boolean value or a vector of boolean values
    based on comparison of its two integer,
    integer vector, pointer, or pointer vector operands.

    :param cond: The condition code indicating the kind of comparison to perform, one of {
        'eq', 'ne', 'ugt', 'uge', 'ult',
        'ule', 'sgt', 'sge', 'slt', 'sle',
        }.
    :type cond: str
    :param result: The converted value.
    :type result: Value
    :param fst_operand: A first operand to compare.
    :type fst_operand: Value
    :param snd_operand: A second operand to compare.
    :type snd_operand: Value
    
    Conversation::
    
        <result> = icmp <cond> <ty> <op1>, <op2>   ; yields i1 or <N x i1>:result
        ICmp(
            cond,
            Value(result, IntegerType(1) or VectorType(N, IntegerType(1))),
            Value(op1, ty),
            Value(op2, ty),
        )
    
    """
    cond: str
    result: Value
    fst_operand: Value
    snd_operand: Value

class FCmp(NamedTuple):
    """
    `FCmp instruction <https://llvm.org/docs/LangRef.html#fcmp-instruction>`_.
    
    The ‘fcmp’ instruction returns a boolean value or vector of boolean values
    based on comparison of its operands.
    
    If the operands are floating-point scalars, then the result type is a boolean (i1).
    
    If the operands are floating-point vectors,
    then the result type is a vector of boolean with the same number of elements
    as the operands being compared.

    :param cond: The condition code indicating the kind of comparison to perform, one of {
        'eq', 'ne', 'ugt', 'uge', 'ult',
        'ule', 'sgt', 'sge', 'slt', 'sle',
        }.
    :type cond: str
    :param result: The converted value.
    :type result: Value
    :param fst_operand: A first operand to compare.
    :type fst_operand: Value
    :param snd_operand: A second operand to compare.
    :type snd_operand: Value
    :param fast_math_flags: A set of fast math flags.
    :type fast_math_flags: frozenset[str]
    
    Conversation::
    
        <result> = icmp [fast-math flags]* <cond> <ty> <op1>, <op2>   ; yields i1 or <N x i1>:result
        ICmp(
            cond,
            Value(result, IntegerType(1) or VectorType(N, IntegerType(1))),
            Value(op1, ty),
            Value(op2, ty),
            {*fast-math flags}
        )
    """
    cond: str
    result: Value
    fst_operand: Value
    snd_operand: Value
    fast_math_flags: frozenset[str] = frozenset()


class Phi(NamedTuple):
    """
    `Phi instruction <https://llvm.org/docs/LangRef.html#phi-instruction>`_.
    
    The ‘phi’ instruction is used to implement
    the φ node in the SSA graph representing the function.

    :param result: A taken value specified by the pair corresponding
        to the predecessor basic block that executed just prior to the current block.
    :type result: Value
    :param vals: A list of pairs of values and predecessor blocks,
        with one pair for each predecessor basic block of the current block.
    :type vals: list[tuple[Value, Value]]
    :param fast_math_flags: A set of fast math flags.
    :type fast_math_flags: frozenset[str]
    
    Conversation::
    
        <result> = phi [fast-math-flags] <ty> [ <val0>, <label0>], ...
        Phi(
            Value(result, Type),
            [
                (Value(val0, ty), Value(label0, LabelType())),
                ...
            ],
            {*fast-math flags}
        )
    """
    result: Value
    vals: list[tuple[Value, Value]]
    fast_math_flags: frozenset[str] = frozenset()


class Select(NamedTuple):
    """
    `Select instruction <https://llvm.org/docs/LangRef.html#select-instruction>`_.
    
    The ‘select’ instruction is used to choose
    one value based on a condition, without IR-level branching.

    :param result: The converted value.
    :type result: Value
    :param cond: A value indicating the condition.
    :type cond: Value
    :param true_value: A value returned if cond is True.
    :type true_value: Value
    :param false_value: A value returned if cond is false.
    :type false_value: Value
    :param fast_math_flags: A set of fast math flags.
    :type fast_math_flags: frozenset[str]
    
    Conversation::
    
        <result> = select [fast-math flags] (i1 or {<N x i1>}) <cond>, <ty> <val1>, <ty> <val2>             ; yields ty
        Select(
            Value(result, ty),
            Value(cond, IntegerType(1) or VectorType(N, IntegerType(1)))
            Value(val1, ty),
            Value(val2, ty),
            {*fast-math flags}
        )
    """
    result: Value
    cond: Value
    true_value: Value
    false_value: Value
    fast_math_flags: frozenset[str] = frozenset()


class Freeze(NamedTuple):
    """
    `Freeze instruction <https://llvm.org/docs/LangRef.html#freeze-instruction>`_.
    
    The ‘freeze’ instruction is used to stop propagation of undef and poison values.

    :param result: An arbitrary fixed value, if the value is undef or poison, otherwise value.
    :type result: Value
    :param value: A value, which can be poison or undef.
    :type value: Value
    
    Conversation::
    
        <result> = freeze ty <val>    ; yields ty:result
        Freeze(
            Value(result, ty),
            Value(val, ty)
        )
    """
    result: Value
    value: Value


class Call(NamedTuple):
    """
    `Call instruction <https://llvm.org/docs/LangRef.html#call-instruction>`_.
    
    The ‘call’ instruction represents a simple function call.

    :param result: The returned value.
    :type result: Value
    :param callee: The function to be invoked, pointer or function name.
    :type callee: Value
    :param args: An argument list.
    :type args: list[Value]
    :param calling_conv: The calling convention that should be used in a call.
    :type calling_conv: CallingConv
    :param call_attrs: A list containing all call-related attributes.
    :type call_attrs: list[Attrs]
    :param tail_kind: A marker indicating that the optimizers
        should perform tail call optimization, one of {'tail', 'musttail', 'notail'}.
    :type tail_kind: str
    :param fast_math_flags: A set of fast math flags.
    :type fast_math_flags: frozenset[str]
    
    Conversation::
    
        <result> = [tail | musttail | notail ] call [fast-math flags] [cconv] [ret attrs] [addrspace(<num>)]
           <ty>|<fnty> <fnptrval>(<function args>) [fn attrs] [ operand bundles ]
        Call(
            Value(result, Type),
            Value(fnptrval, FunctionType | Type),
            [
                Value(arg0, Type),
                Value(arg1, Type),
                ...
            ],
            "tail" | "musttail" | "notail" | None
            cconv,
            [call_attrs]
            {*fast-math flags}
        )
    """
    result: Value
    callee: Value
    args: list[Value]
    calling_conv: CallingConv
    call_attrs: list[Attrs]
    tail_kind: str | None = None
    fast_math_flags: frozenset[str] = frozenset()


class VaArg(NamedTuple):
    """
    `VaArg instruction <https://llvm.org/docs/LangRef.html#va-arg-instruction>`_.
    
    The ‘va_arg’ instruction is used to access arguments passed
    through the “variable argument” area of a function call.
    It is used to implement the va_arg macro in C.

    :param result: The va_list* value.
    :type result: Value
    :param value: The value of the specified argument type.
    :type value: Value
    
    Conversation::
    
        <resultval> = va_arg <va_list*> <arglist>, <argty>
        VaArg(
            Value(resultval, argty),
            Value(arglist, PtrType(...))
        )
    """
    result: Value
    value: Value


class LandingPad(NamedTuple):
    """
    `LandingPad instruction <https://llvm.org/docs/LangRef.html#landingpad-instruction>`_.
    
    The ‘landingpad’ instruction is used by LLVM’s exception handling system
    to specify that a basic block is a landing pad — one where the exception lands,
    and corresponds to the code found in the catch portion of a try/catch sequence.
    It defines values supplied by the personality function upon re-entry to the function.
    The resultval has the type resultty.

    :param result: https://llvm.org/docs/LangRef.html#landingpad-instruction
    :type result: Value
    :param is_cleanup: If True, the landing pad block is a cleanup.
    :type is_cleanup: bool
    :param is_catchs: A list indicating which clauses are catch-type,
        in the same order as clauses, you can use zip(is_catchs, clauses).
    :type is_catchs: list[bool]
    :param clauses: A list of clauses.
    :type clauses: list[Value]
    
    Conversation::
    
        <resultval> = landingpad <resultty> <clause>+
        <clause> := catch <type> <value>
        <clause> := filter <array constant type> <array constant>
        LangingPad(
            Value(resultval, Type),
            False,
            [True if clause is catch else False, ...]
            [Value(value, type), ...]
        )
        
        <resultval> = landingpad <resultty> cleanup <clause>*
        LangingPad(
            Value(resultval, Type),
            True,
            [True if clause is catch else False, ...]
            [Value(value, type), ...]
        )
    """
    result: Value
    is_cleanup: bool
    is_catchs: list[bool]
    clauses: list[Value]


class CatchPad(NamedTuple):
    """
    `CatchPad instruction <https://llvm.org/docs/LangRef.html#catchpad-instruction>`_.
    
    The ‘catchpad’ instruction is used by LLVM’s exception handling system
    to specify that a basic block begins a catch handler — one where
    a personality routine attempts to transfer control to catch an exception.

    :param result: The token, used to match the catchpad to corresponding catchrets
        and other nested EH pads.
    :type result: Value
    :param catchswith: A token produced by a catchswitch instruction in a predecessor block.
    :type catchswith: Value
    :param args: A list corresponding to whatever information the personality routine requires
        to know if this is an appropriate handler for the exception.
    :type args: list[Value]
    
    Conversation::
    
        <resultval> = catchpad within <catchswitch> [<args>*]
        CatchPad(
            Value(resultval, TokenType()),
            Value(catchswitch, TokenType()),
            [
                Value(arg0, Type),
                Value(arg1, Type),
                ...
            ]
        )
    """
    result: Value
    catchswith: Value
    args: list[Value]


class CleanupPad(NamedTuple):
    """
    `CleanupPad instruction <https://llvm.org/docs/LangRef.html#cleanuppad-instruction>`_.
    
    The ‘cleanuppad’ instruction is used by LLVM’s exception handling system
    to specify that a basic block is a cleanup block — one where a personality
    routine attempts to transfer control to run cleanup actions.
    The args correspond to whatever additional information the personality
    function requires to execute the cleanup. The resultval has the type token
    and is used to match the cleanuppad to corresponding cleanuprets.
    The parent argument is the token of the funclet that contains the cleanuppad instruction.
    If the cleanuppad is not inside a funclet, this operand may be the token none.

    :param result: A token, used to match the cleanuppad to corresponding cleanuprets.
    :type result: Value
    :param parent: The token of the funclet that contains the cleanuppad instruction.
        If the cleanuppad is not inside a funclet, this operand may be the token none.
    :type parent: Value
    :param args: A list corresponding to whatever additional information the
        personality function requires to execute the cleanup.
    :type args: list[Value]
    
    Conversation::
    
        <resultval> = cleanuppad within <parent> [<args>*]
        CleanupPad(
            Value(resultval, TokenType()),
            Value(parent, TokenType()),
            [
                Value(arg0, Type),
                Value(arg1, Type),
                ...
            ]
        )
    """
    result: Value
    parent: Value
    args: list[Value]

# fmt: on

Instruction = (
    Ret
    | Br
    | Switch
    | IndirectBr
    | Invoke
    | Resume
    | CallBr
    | CatchSwitch
    | CatchRet
    | CleanupPad
    | Unreacheble
    | UnaryOp
    | BinOp
    | ExtractElement
    | InsertElement
    | ShuffleVector
    | ExtractValue
    | InsertValue
    | Alloca
    | Load
    | Store
    | Fence
    | CmpXchg
    | AtomicRmw
    | GetElementPtr
    | Conversion
    | ICmp
    | FCmp
    | Phi
    | Select
    | Freeze
    | Call
    | VaArg
    | LandingPad
    | CatchPad
    | CleanupPad
)

Constructor = Callable[
    [
        list[Value],  # operands
        Value,  # Value
        str,  # opcode name
        tuple,  # additional data
        Any,  # attributes
    ],
    Iterable,
]

_binop_constructor = lambda operands, value, opcode, _, attrs: (
    opcode,
    value,
    *operands,
    frozenset(attrs.get("fmf", [])),
    "nuw" in attrs,
    "nsw" in attrs,
    "exact" in attrs,
    "disjoint" in attrs,
)

_conversion_constructor = lambda operands, value, opcode, _, attrs: (
    opcode,
    value,
    operands[0],
    frozenset(attrs.get("fmf", [])),
    "nuw" in attrs,
    "nsw" in attrs,
)

_constructors: list[tuple[Any, Constructor]] = [
    # 1
    (
        Ret,
        lambda operands, *_: (operands if len(operands) != 0 else (None,)),
    ),
    # 2
    (
        Br,
        lambda operands, *_: (
            (None, *operands, None) if (len(operands) == 1) else operands
        ),
    ),
    # 3
    (
        Switch,
        lambda operands, *_: (
            operands[0],
            operands[1],
            list(zip(operands[2::2], operands[3::2])),
        ),
    ),
    # 4
    (
        IndirectBr,
        lambda operands, *_: (operands[0], operands[1:]),
    ),
    # 5
    (
        Invoke,
        lambda operands, value, unused, additional, *_: (
            value,
            operands[-1],
            operands[:-3],
            operands[-3],
            operands[-2],
            CallingConv(additional[0]),
            attrs_list_to_dict(additional[1]),
        ),
    ),
    # 6
    (
        Resume,
        lambda operands, *_: operands,
    ),
    # 7
    (Unreacheble, lambda *_: []),
    # 8
    (CleanupRet, lambda operands, *_: operands),
    # 9
    (
        CatchRet,
        lambda operands, *_: operands,
    ),
    # 10
    (
        CatchSwitch,
        lambda operands, value, unused, additional, *_: (
            (value, operands[0], operands[2:], operands[1])
            if additional[0]
            else (value, operands[0], operands[1:], None)
        ),
    ),
    # 11
    (
        CallBr,
        lambda operands, value, unused, additional, *_: (
            value,
            operands[-1],
            operands[: -additional[2] - 2],
            operands[-additional[2] - 2],
            operands[-additional[2] - 1 : -1],
            CallingConv(additional[0]),
            attrs_list_to_dict(additional[1]),
        ),
    ),
    # unary, 12
    (
        UnaryOp,
        lambda operands, value, opcode, unused, attrs: (
            opcode,
            value,
            operands[0],
            frozenset(attrs.get("fmf", [])),
        ),
    ),
    # binary, 13
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    # bitwise, 25
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    (BinOp, _binop_constructor),
    # memory, 31
    (
        Alloca,
        lambda operands, value, unused, additional, attrs: (
            value,
            additional[0],
            operands[0],
            attrs.get("align", 0),
            "inalloca" in attrs,
        ),
    ),
    (
        Load,
        lambda operands, value, unused, unused1, attrs: (
            value,
            operands[0],
            attrs.get("align", 0),
            "volatile" in attrs,
            "atomic" in attrs,
            Ordering(attrs.get("ordering", Ordering.NotAtomic)),
            attrs.get("syncscope", None),
        ),
    ),
    (
        Store,
        lambda operands, unused, unused1, unused2, attrs: (
            *operands,
            attrs.get("align", 0),
            "volatile" in attrs,
            "atomic" in attrs,
            Ordering(attrs.get("ordering", Ordering.NotAtomic)),
            attrs.get("syncscope", None),
        ),
    ),
    (
        GetElementPtr,
        lambda operands, value, unused, additional, attrs: (
            value,
            additional[1],
            operands[0],
            operands[1:],
            additional[0],
            "inbounds" in attrs,
        ),
    ),
    (
        Fence,
        lambda unused, unused1, unused2, unused3, attrs: (
            Ordering(attrs.get("ordering", Ordering.NotAtomic)),
            attrs.get("syncscope", None),
        ),
    ),
    (
        CmpXchg,
        lambda operands, value, unused, additional, attrs: (
            value,
            *operands,
            Ordering(additional[0]),
            Ordering(additional[1]),
            attrs.get("align", 0),
            "weak" in attrs,
            "volatile" in attrs,
            attrs.get("syncscope", None),
        ),
    ),
    (
        AtomicRmw,
        lambda operands, value, unused, additional, attrs: (
            additional[0],
            value,
            *operands,
            Ordering(attrs.get("ordering", Ordering.NotAtomic)),
            attrs.get("align", 0),
            "volatile" in attrs,
            attrs.get("syncscope", None),
        ),
    ),
    # conversion, 38
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    (Conversion, _conversion_constructor),
    # pads, 51
    (
        CleanupPad,
        lambda operands, value, *_: (value, operands[-1], operands[:-1]),
    ),
    (
        CatchPad,
        lambda operands, value, *_: (value, operands[-1], operands[:-1]),
    ),
    # other, 53
    (
        ICmp,
        lambda operands, value, unused, additional, attrs: (
            additional[0],
            value,
            *operands,
        ),
    ),
    (
        FCmp,
        lambda operands, value, unused, additional, attrs: (
            additional[0],
            value,
            *operands,
            frozenset(attrs.get("fmf", [])),
        ),
    ),
    (
        Phi,
        lambda operands, value, unused, additional, attrs: (
            value,
            list(zip(operands, additional[0])),
            frozenset(attrs.get("fmf", [])),
        ),
    ),
    (
        Call,
        lambda operands, value, unused, additional, attrs: (
            value,
            operands[-1],
            operands[:-1],
            CallingConv(additional[0]),
            attrs_list_to_dict(additional[1]),
            attrs.get("tailkind", None),
            frozenset(attrs.get("fmf", [])),
        ),
    ),
    (
        Select,
        lambda operands, value, unused, additional, attrs: (
            value,
            *operands,
            frozenset(attrs.get("fmf", [])),
        ),
    ),
    # user ops, 58
    (NotImplemented, lambda *_: []),
    (NotImplemented, lambda *_: []),
    # 60
    (VaArg, lambda operands, value, *_: (value, *operands)),
    # vector, 61
    (ExtractElement, lambda operands, value, *_: (value, *operands)),
    (InsertElement, lambda operands, value, *_: (value, *operands)),
    (
        ShuffleVector,
        lambda operands, value, unused, additional, *_: (
            value,
            *operands,
            additional[0],
        ),
    ),
    # aggregate, 64
    (
        ExtractValue,
        lambda operands, value, unused, additional, *_: (
            value,
            operands[0],
            additional[0],
        ),
    ),
    (
        InsertValue,
        lambda operands, value, unused, additional, *_: (
            value,
            *operands,
            additional[0],
        ),
    ),
    (
        LandingPad,
        lambda operands, value, unused, additional, *_: (
            value,
            additional[0],
            additional[1],
            operands,
        ),
    ),
    (Freeze, lambda operands, value, unused, additional, *_: (value, operands[0])),
]


def _create_instruction(
    opcode: int,
    opcode_name: str,
    operands: list[Value],
    additional: tuple,
    attributes: list[tuple],
    value: Value,
):
    attributes_dict = attrs_to_dict(attributes)
    constructor, make_params = _constructors[opcode - 1]
    params = make_params(operands, value, opcode_name, additional, attributes_dict)
    r = constructor(*params)
    return r
