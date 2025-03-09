from llvm2py import parse_assembly
from llvm2py.ir import *
from graphviz import Digraph


with open("../test_files/factorial.ll") as file:
    source = file.read()

mod = parse_assembly(source)

g = Digraph()

node_attributes = {"shape": "record", "style": "filled"}


def name_label(label):
    return label.replace("%", "\\%")


def name_block(block):
    name = block.value.val
    return name_label(name)


for block in mod.funcs["factorial_req"].blocks.values():
    color = "#f59c7d70"  # Default block color
    last_instruction = block.instrs[-1]

    match last_instruction:
        case Br(None, Value(label)):
            g.edge(name_block(block), name_label(label))
        case Br(_, Value(label_false), Value(label_true)):
            g.edge(name_block(block), name_label(label_true), label="True")
            g.edge(name_block(block), name_label(label_false), label="False")

    if len(block.pred_blocks) >= 2:
        color = "#b70d2870"  # merge-type block

    g.node(name_block(block), **node_attributes, color=color)

g.save("cfg.dot")
