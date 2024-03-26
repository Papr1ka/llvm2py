import json
from typing import Tuple, Dict
from .function import Function
from pprint import pprint
from pprint import pformat

class Module:
    __functions: Dict[str, Function]
    __functions_tuple: Tuple[Function]
    _fields = (
        'functions',
        'name',
        'type_'
    )

    def __init__(self, functions: Tuple[Function]):
        self.__functions = {function.name: function for function in functions}
        self.__functions_tuple = functions

    def get_function(self, name: str):
        return self.__functions.get(name)

    @property
    def functions(self):
        return self.__functions_tuple
