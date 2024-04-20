from typing import Tuple

from .value import Value


class Argument(Value):
    # Argument position in function arguments, starting from zero
    position: int
    _fields = (
        'position',
        'name',
        'type_'
    )

    def __init__(self, position, value_args: Tuple):
        super().__init__(*value_args)
        self.position = position

    def __repr__(self) -> str:
        return f"<Argument position={self.position}, name={self.name}, type={self.type_}, parent={self.parent.name}>"
