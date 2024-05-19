from llpy import ir
from llpy import parse_assembly
from graphviz import Digraph


with open("../test_files/factorial.ll") as file:
    ll = file.read()

mod: ir.Module = parse_assembly(ll)

g = Digraph()

node_attributes = {
    "shape": "record",
    "style": "filled"
}


def graph_node(node: ir.Value):
    text = str(node).replace('\n', '\\n\n')
    return node.name[1:], node.name + ":" + text


for block in mod.get_function("factorial_req").blocks:
    color = "#f59c7d70"  # Цвет блока по умолчанию
    last_instruction = block.instructions[-1]

    if last_instruction.op_code_name == "br":
        operands = last_instruction.operands
        if len(operands) == 3:
            g.edge(block.name[1:], operands[1].name[1:], label="True")
            g.edge(block.name[1:], operands[2].name[1:], label="False")
            color = "#b70d2870"  # switch-type block
        else:
            g.edge(block.name[1:], operands[0].name[1:])
    if len(block.pred_blocks) >= 2:
        color = "#b70d2870"  # merge-type block

    g.node(*graph_node(block), **node_attributes, color=color)

g.save("cfg.dot")
