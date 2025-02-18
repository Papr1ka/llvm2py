from typing import Callable

from . import ir
from ._llvm2py import parse_assembly


parse_assembly: Callable[[str], ir.Module]

__version__ = "0.1.0b"
