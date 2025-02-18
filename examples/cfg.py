from llvm2py import ir
from llvm2py import parse_assembly
from graphviz import Digraph

from llvm2py.ir.instruction import *


with open("../test_files/factorial.ll") as file:
    ll = file.read()

mod: ir.Module = parse_assembly(ll)

g = Digraph()

node_attributes = {"shape": "record", "style": "filled"}


def graph_node(node):
    text = str(node).replace("\n", "\\n\n")
    return node.value.val[1:], text


for block in mod.get_function("factorial_req").blocks:
    color = "#f59c7d70"  # Default block color
    last_instruction = block.instrs[-1]

    if last_instruction.opcode == "br":
        if last_instruction.cond is not None:
            g.edge(
                block.value.val[1:], last_instruction.label_true.val[1:], label="True"
            )
            g.edge(
                block.value.val[1:], last_instruction.label_false.val[1:], label="False"
            )
            color = "#b70d2870"  # switch-type block
        else:
            g.edge(block.value.val[1:], last_instruction.label_false.val[1:])
    if len(block.pred_blocks) >= 2:
        color = "#b70d2870"  # merge-type block

    g.node(*graph_node(block), **node_attributes, color=color)

g.save("cfg.dot")
