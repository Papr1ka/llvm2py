from llpy import ir
from llpy import parse_assembly
from llpy.utils import dump


with open("test_files/factorial.ll") as file:
    ir_text = file.read()

mod: ir.Module = parse_assembly(ir_text)

with open("dump.txt", "w") as file:
    file.write(dump(mod.get_function("factorial_req"), indent=4, annotate_fields=False))
