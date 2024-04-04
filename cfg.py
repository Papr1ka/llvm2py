from llvm_python import ir as IR
from llvm_python import parse_assembly
from graphviz import Digraph

with open("./test_files/factorial.ll") as file:
    ir = file.read()

mod: IR.Module = parse_assembly(ir)

g = Digraph()

print(mod.get_function("factorial_req").blocks)

def graph_node(node: IR.Value):
    return node.name[1:], node.name + ":\n\n" + str(node)


for function in mod.functions:
    if function.name != "factorial_req": continue
    for block in function.blocks:
        g.node(*graph_node(block))
        last_instruction = block.instructions[-1]
        if last_instruction.op_code_name == "br":
            f = last_instruction.operands
            print([i.name for i in f])
            for i in range(len(f)):
                operand = f[i]

                if i == 1:
                    label = "True"
                else:
                    label = "False"

                g.node(*graph_node(block))
                g.node(*graph_node(operand))
                if len(last_instruction.operands) > 2:
                    g.edge(block.name[1:], operand.name[1:], label=label)
                else:
                    g.edge(block.name[1:], operand.name[1:])

print("#" * 20)

# for function in mod.functions:
#     for block in function.blocks:
#         for instruction in block.instructions:
#             if (len(instruction.operands) >= 2):
#                 print(instruction.op_code_name, [i.name for i in instruction.operands])
#             # for operand in instruction.operands:


g.save("test.dot")
