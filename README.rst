|PyPI| |Actions Status| |Release|

llvm2py
#######

`Documentation is available here <https://papr1ka.github.io/llvm2py/>`_

A fairly large proportion of programs are written in C/C++.

Let's imagine that you need to analyze programs in a given language, to search for vulnerabilities, to detect patterns or for optimization purposes.
To solve such a problem, it is necessary to have the code in a slightly more convenient form than the source code of the program - an intermediate representation.

You might come up with the idea of building your own compiler, which is quite difficult, or you might decide to use intermediate representations of GCC or LLVM, but in that case you have to deal with the C/C++ API, which is something you don't want when you have elegant solutions in Python.

**llvm2py** allows you to analyze C/C++ programs in the LLVM IR representation in Python.

.. note::
    
    The library is in beta, so in case of problems, feel free to create issues.


Usage example
-------------

The following example will build a control flow graph for the following function.

.. code-block:: cpp

    int factorial_req(int n)
    {
        if (n == 1)
        {
            return 1;
        }
        return factorial_req(n - 1) * n;
    }

.. code-block:: llvm

    define dso_local i32 @factorial_req(i32 noundef %0) {
        %2 = alloca i32, align 4
        %3 = alloca i32, align 4
        store i32 %0, ptr %3, align 4
        %4 = load i32, ptr %3, align 4
        %5 = icmp eq i32 %4, 1
        br i1 %5, label %6, label %7

    6:                                                ; preds = %1
        store i32 1, ptr %2, align 4
        br label %13

    7:                                                ; preds = %1
        %8 = load i32, ptr %3, align 4
        %9 = sub nsw i32 %8, 1
        %10 = call i32 @factorial_req(i32 noundef %9)
        %11 = load i32, ptr %3, align 4
        %12 = mul nsw i32 %10, %11
        store i32 %12, ptr %2, align 4
        br label %13

    13:                                               ; preds = %7, %6
        %14 = load i32, ptr %2, align 4
        ret i32 %14
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
