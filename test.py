import llvm_python
from llvm_python import parse_assembly
from llvm_python.utils import dump

with open("./test_files/factorial_opt.ll") as file:
    ll = file.read()    


module: llvm_python.ir.Module = parse_assembly(ll)
function = module.get_function("factorial_cycle")
block = function.get_block("%7")

#print(block)
levels = [[] for i in range(len(block.instructions))]
for i in range(len(block.instructions) - 1, -1, -1):
    instruction = block.instructions[i]

    levels[i].append(instruction.name)
    levels[i - 1].extend([i.name for i in instruction.operands])
    for operands in instruction.operands:
        print(operands)
    print(instruction)

print(levels)
