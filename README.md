[![PyPI](https://img.shields.io/pypi/v/llvm2py.svg)](https://pypi.python.org/pypi/llvm2py)
[![Actions status](https://github.com/Papr1ka/llvm2py/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Papr1ka/llvm2py/actions/workflows/main.yml)
[![release](https://img.shields.io/github/v/release/Papr1ka/llvm2py.svg?label=release)](https://github.com/Papr1ka/llvm2py/releases)


# llvm2py

A fairly large proportion of programs are written in C/C++.

Let's imagine that you need to analyze programs in a given language, to search for vulnerabilities, to detect patterns or for optimization purposes.
To solve such a problem, it is necessary to have the code in a slightly more convenient form than the source code of the program - an intermediate representation.

You might come up with the idea of building your own compiler, which is quite difficult, or you might decide to use intermediate representations of GCC or LLVM, but in that case you have to deal with the C/C++ API, which is something you don't want when you have elegant solutions in Python.

**llvm2py** allows you to analyze C/C++ programs in the LLVM IR representation in Python.

> The library is in beta, so in case of problems, feel free to create issues.


# Usage example

The following example will build a control flow graph for the following function [factorial.c](./test_files/factorial.c), [factorial.ll](./test_files/factorial.ll).

```cpp
int factorial_req(int n)
{
    if (n == 1)
    {
        return 1;
    }
    return factorial_req(n - 1) * n;
}
```

```python
from llvm2py import ir
from llvm2py import parse_assembly
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
    text = str(node).replace("\n", "\l")
    return node.name[1:], node.name + ":" + text


for block in mod.get_function("factorial_req").blocks:
    color = "#f59c7d70"  # Default block color
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
```

# Installation

## Preferred way

`pip install llvm2py`

Supported versions

CPython3.7 - CPython3.12

On Windows 64bit and manylinux x86_64 platforms.

## Manual installation

1. Dependencies

* For correct build you need **CMake >= 3.27**

* C and C++ compilers.

* The system must also have libraries `libffi` и `libtinfo`.

> If the libraries are not found, you can add them manually, example [CMakeLists.txt](./CMakeLists.txt), lines 12-15.

* Preferred build system **Ninja**

2. Cloning llvm2py

`git clone git@github.com:Papr1ka/llvm2py.git`

`cd llvm2py`

3. LLVM setup

You must have the static library **LLVM** version >= 16 installed on the system.

### This can be done via the distribution's package manager.

Example:

`sudo dnf install llvm`

`sudo dnf install llvm-devel`

### Or you can build LLVM manually and specify the path to the cmake folder, line 21

`LLVM_DIR = "/usr/lib/llvm-18/cmake" # Path to cmake folder of llvm library`

### Or you can download compiled libraries

* Deb пакеты https://apt.llvm.org/
* Windows https://packages.msys2.org/package/mingw-w64-x86_64-llvm

4. Run setup.py

in the directory with setup.py:

`python -m pip install .`
