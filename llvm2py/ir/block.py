from typing import NamedTuple
from .instruction import CallBr, Instruction, Call, Invoke
from .value import Value


class Block(NamedTuple):
    """
    Basic block class.

    :param value: The block as value.
    :type value: Value
    :param instrs: A list of block instructions.
    :type instrs: list[Instruction]
    :param pred_blocks: A list of predecessor block names.
    :type pred_blocks: list[str]
    """

    value: Value

    instrs: list[Instruction]

    pred_blocks: list[str]

    def has_no_calls(self):
        """
        Returns true if the block does not contain calls to other functions.

        Intrinsics are not considered functions.
        """
        for instr in self.instrs:
            match instr:
                case (
                    Call(_, Value(str(callee)))
                    | CallBr(_, Value(str(callee)))
                    | Invoke(_, Value(str(callee)))
                ):
                    """
                    Intrinsic function names must all start with an “llvm.” prefix.
                    https://llvm.org/docs/LangRef.html#intrinsic-functions
                    """
                    if not callee.startswith("llvm."):
                        return False
        return True
