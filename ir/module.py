from typing import Tuple
from .function import Function


class Module:
    name: str
    functions: Tuple[Function]

    def __str__(self):
        return self.name

    def dict(self):
        return {function.name: function for function in self.functions}