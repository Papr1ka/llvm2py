from typing import Callable

from . import ir
from . import utils
from ._llvm2py import parse_assembly


parse_assembly: Callable[
    [str],
    ir.Module
]

__version__ = "0.0.1b2"
