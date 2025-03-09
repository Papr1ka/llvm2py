IR Structure
============

To work with this library it is advisable to be familiar with LLVM IR, but if you are not, here is a brief introduction.

The LLVM implementation contains a huge number of classes, llvm2py does not implement them all, generalizing many things.

.. image:: ./ir.png

A module is a translation unit of the input programs and consists of functions and global variables

At this time, metadata, aliases, ifuncs and comdats are not supported.

A function definition contains a list of basic blocks, forming the CFG (Control Flow Graph) for the function.

Basic block contains a list of instructions that are executed linearly, and ends with a terminator instruction.

The instruction contains a list of operands (not always), which are values.

In an LLVM implementation, both the instruction, basic blocks and functions are values (inheritance relation).

This fact is realized through the value attribute in each of the classes described, so that classes have a reference to a value.

Global variables, as well as functions in the LLVM implementation, inherit from GlobalObject, and the latter from GlobalValue, accumulating many attributes from them. Many such attributes are collected in the GlobalObject class.

Each value has a type. Composite types are recursive.

A more detailed description of each class can be found in their documentation.

It's also worth looking at the handling of attributes :doc:`about_attributes`.

And you can learn about LLVM IR from here https://llvm.org/docs/LangRef.html.
