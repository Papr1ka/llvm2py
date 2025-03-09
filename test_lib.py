import unittest
from llvm2py import parse_assembly


with open("./test.ll") as file:
    source = file.read()
