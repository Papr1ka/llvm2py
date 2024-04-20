from typing import Callable

from . import ir
from . import utils
from ._llvm_python import parse_assembly


parse_assembly: Callable[
    [str],
    ir.Module
]
