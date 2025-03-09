"""
This module contains all types that exist in the LLVM IR representation.
For detailed documentation, please refer to the source https://llvm.org/docs/LangRef.html#type-system
"""

from __future__ import annotations
from typing import NamedTuple


class VoidType(NamedTuple):
    def __str__(self):
        return "void"


class FunctionType(NamedTuple):
    """
    :param param_tys: List of function argument types in the appropriate order.
    :type param_tys: list[Type]
    :param ret_ty: Type of value returned by function.
    :type ret_ty: Type
    """

    param_tys: list[Type]
    ret_ty: Type

    def __str__(self):
        return f"{self.ret_ty} ({', '.join(map(str, self.param_tys))})"


class IntegerType(NamedTuple):
    """
    :param num_bits: Bit width.
    :type num_bits: int
    """

    num_bits: int

    def __str__(self):
        return f"i{self.num_bits}"


class FPType(NamedTuple):
    """
    :param kind: One of {'half', 'bfloat', 'float', 'double', 'fp128', 'x86_fp80', 'ppc_fp128'}
    :type kind: str
    """

    kind: str

    def __str__(self):
        return self.kind


class X86_amxType(NamedTuple):
    def __str__(self):
        return "x86_amx"


class PtrType(NamedTuple):
    """
    Almost always, pointers are opaque (untyped).

    :param addr_space: Numbered address space where the pointed-to object resides.
    :type addr_space: int
    :param ty: Pointer type (may be used by some gpu targets).
    :type ty: Type | None
    """

    addr_space: int
    ty: Type | None = None

    def __str__(self):
        if self.ty is not None:
            return f"ptr: {self.ty}"
        else:
            return "ptr"


class TargetExtensionType(NamedTuple):
    """
    :param name: Type name.
    :type name: str
    :param params: List of type parameters.
    :type params: list[int | Type]
    """

    name: str
    params: list[int | Type]

    def __str__(self):
        name = ['"' + self.name + '"']
        return f"target({', '.join(map(str, name + self.params))})"


class VectorType(NamedTuple):
    """
    :param elem_count: Vector element count. If the vector is scalable, it is the minimum number of elements in this vector.
        The actual number of elements in the vector is an integer multiple of this value.
    :type elem_count: int
    :param elem_ty: Vector element type.
    :type elem_ty: Type
    :param is_scalable: If True, the vector is scalable (vscale).
    :type is_scalable: bool
    """

    elem_count: int
    elem_ty: Type
    is_scalable: bool = False

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
    """
    :param elem_count: The number of elements in the array.
    :type elem_count: int
    :param elem_ty: The array element type.
    :type elem_ty: Type
    """

    elem_count: int
    elem_ty: Type

    def __str__(self):
        return f"[{self.elem_count} x {self.elem_ty}]"


class StructureType(NamedTuple):
    """
    :param name: Structure name, if it is a named structure.
    :type name: str | None
    :type elem_tys: List of structure types.
    :type elem_tys: list[Type]
    :type is_packed: If True, the structure is packed,
        which indicate that the alignment of the struct is one byte and
        there is no padding between the elements.
    :type is_packed: bool
    """

    name: str | None
    elem_tys: list[Type]
    is_packed: bool = False

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
