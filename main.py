from llvm_python import ir
from llvm_python import parse_assembly
from llvm_python.utils import dump


with open("test_files/factorial.ll") as file:
    ir_text = file.read()

mod: ir.Module = parse_assembly(ir_text)

with open("dump.txt", "w") as file:
    file.write(dump(mod.get_function("factorial_req"), indent=4, annotate_fields=False))
