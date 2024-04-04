from llvm_python import ir as IR
from llvm_python import parse_assembly
from llvm_python.utils import dump


with open("test_files/factorial.ll") as file:
    ir = file.read()

mod: IR.Module = parse_assembly(ir)


with open("dump.txt", "w") as file:
    file.write(dump(mod, indent=4, annotate_fields=False))
