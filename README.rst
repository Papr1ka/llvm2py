|PyPI| |Actions Status| |Release|

llvm2py
#######

A fairly large proportion of programs are written in C/C++.

Let's imagine that you need to analyze programs in a given language, to search for vulnerabilities, to detect patterns or for optimization purposes.
To solve such a problem, it is necessary to have the code in a slightly more convenient form than the source code of the program - an intermediate representation.

You might come up with the idea of building your own compiler, which is quite difficult, or you might decide to use intermediate representations of GCC or LLVM, but in that case you have to deal with the C/C++ API, which is something you don't want when you have elegant solutions in Python.

**llvm2py** allows you to analyze C/C++ programs in the LLVM IR representation in Python.

.. note::
    
    The library is in beta, so in case of problems, feel free to create issues.


Usage example
-------------

The following example will build a control flow graph for the following function [factorial.c](./test_files/factorial.c), [factorial.ll](./test_files/factorial.ll).

.. code-block:: cpp

    int factorial_req(int n)
    {
        if (n == 1)
        {
            return 1;
        }
        return factorial_req(n - 1) * n;
    }

.. code-block:: python

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

.. |PyPI| image:: https://img.shields.io/pypi/v/llvm2py.svg
    :target: https://pypi.python.org/pypi/llvm2py

.. |Actions status| image:: https://github.com/Papr1ka/llvm2py/actions/workflows/main.yml/badge.svg?branch=main
    :target: https://github.com/Papr1ka/llvm2py/actions/workflows/main.yml

.. |Release| image:: https://img.shields.io/github/v/release/Papr1ka/llvm2py.svg?label=release
    :target: https://github.com/Papr1ka/llvm2py/releases
