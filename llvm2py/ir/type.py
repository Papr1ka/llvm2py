from __future__ import annotations
from typing import NamedTuple


class VoidType(NamedTuple):
    def __str__(self):
        return "void"


class FunctionType(NamedTuple):
    param_tys: list[Type]
    ret_ty: Type

    def __str__(self):
        return f"{self.ret_ty} ({', '.join(map(str, self.param_tys))})"


class IntegerType(NamedTuple):
    num_bits: int

    def __str__(self):
        return f"i{self.num_bits}"


class FPType(NamedTuple):
    kind: str

    def __str__(self):
        return self.kind


class X86_mmxType(NamedTuple):
    def __str__(self):
        return "x86_mmx"


class X86_amxType(NamedTuple):
    def __str__(self):
        return "x86_amx"


class PtrType(NamedTuple):
    addr_space: str
    ty: Type | None

    def __str__(self):
        if self.ty is not None:
            return f"ptr: {self.ty}"
        else:
            return "ptr"


class TargetExtensionType(NamedTuple):
    name: str
    params: list[int | Type]

    def __str__(self):
        name = ['"' + self.name + '"']
        return f"target({', '.join(map(str, name + self.params))})"


class VectorType(NamedTuple):
    elem_count: int
    elem_ty: Type
    is_scalable: bool

    def __str__(self):
        if self.is_scalable:
            return f"<vscale x {self.elem_count} x {self.elem_ty}>"
        else:
            return f"<{self.elem_count} x {self.elem_ty}>"


class LabelType(NamedTuple):
    def __str__(self):
        return "label"


class TokenType(NamedTuple):
    def __str__(self):
        return "token"


class MetadataType(NamedTuple):
    def __str__(self):
        return "metadata"


class ArrayType(NamedTuple):
    elem_count: int
    elem_ty: Type

    def __str__(self):
        return f"[{self.elem_count} x {self.elem_ty}]"


class StructureType(NamedTuple):
    name: str | None
    elem_tys: list[Type]
    is_packed: bool

    def __str__(self):
        if self.is_packed:
            return f"<{{{', '.join(map(str, self.elem_tys))}}}>"
        else:
            return f"{{{', '.join(map(str, self.elem_tys))}}}"


class OpaqueType(NamedTuple):
    def __str__(self):
        return "opaque"


Type = (
    VoidType
    | FunctionType
    | IntegerType
    | FPType
    | X86_amxType
    | PtrType
    | TargetExtensionType
    | VectorType
    | LabelType
    | TokenType
    | MetadataType
    | ArrayType
    | StructureType
    | OpaqueType
)
