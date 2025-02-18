from typing import Callable

from . import ir
from ._llvm2py import parse_assembly


parse_assembly: Callable[[str], ir.Module]

<<<<<<< HEAD
__version__ = "0.1.0b"
=======
__version__ = "0.0.1b3"
>>>>>>> main
