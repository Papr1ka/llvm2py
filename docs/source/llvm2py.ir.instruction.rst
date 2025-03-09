llvm2py.ir.instruction module
=============================

Terminator instructions
-----------------------

Every basic block in a program ends with a “Terminator” instruction,
which indicates which block should be executed after the current block is finished.

.. autoclass:: llvm2py.ir.instruction.Ret
.. autoclass:: llvm2py.ir.instruction.Br
.. autoclass:: llvm2py.ir.instruction.Switch
.. autoclass:: llvm2py.ir.instruction.IndirectBr
.. autoclass:: llvm2py.ir.instruction.Invoke
.. autoclass:: llvm2py.ir.instruction.CallBr
.. autoclass:: llvm2py.ir.instruction.Resume
.. autoclass:: llvm2py.ir.instruction.CatchSwitch
.. autoclass:: llvm2py.ir.instruction.CatchRet
.. autoclass:: llvm2py.ir.instruction.CleanupRet
.. autoclass:: llvm2py.ir.instruction.Unreacheble

Unary operations
----------------

.. autoclass:: llvm2py.ir.instruction.UnaryOp

Binary operations
-----------------

.. autoclass:: llvm2py.ir.instruction.BinOp

Vector operations
-----------------

Instructions representing vector operations in a target-independent manner.

.. autoclass:: llvm2py.ir.instruction.ExtractElement
.. autoclass:: llvm2py.ir.instruction.InsertElement
.. autoclass:: llvm2py.ir.instruction.ShuffleVector

Aggregate operations
--------------------

Instructions for working with aggregate values.

.. autoclass:: llvm2py.ir.instruction.ExtractValue
.. autoclass:: llvm2py.ir.instruction.InsertValue

Memory access and addressing operations
---------------------------------------

A key design point of an SSA-based representation is how it represents memory.
In LLVM IR, no memory locations are in SSA form, which makes things very simple.
This section describes how to read, write, and allocate memory in LLVM IR.

.. autoclass:: llvm2py.ir.instruction.Alloca
.. autoclass:: llvm2py.ir.instruction.Load
.. autoclass:: llvm2py.ir.instruction.Store
.. autoclass:: llvm2py.ir.instruction.CmpXchg
.. autoclass:: llvm2py.ir.instruction.AtomicRmw
.. autoclass:: llvm2py.ir.instruction.GetElementPtr

Conversion operations
---------------------

.. autoclass:: llvm2py.ir.instruction.Conversion

Other operations
----------------

.. autoclass:: llvm2py.ir.instruction.ICmp
.. autoclass:: llvm2py.ir.instruction.FCmp
.. autoclass:: llvm2py.ir.instruction.Phi
.. autoclass:: llvm2py.ir.instruction.Select
.. autoclass:: llvm2py.ir.instruction.Freeze
.. autoclass:: llvm2py.ir.instruction.Call
.. autoclass:: llvm2py.ir.instruction.VaArg
.. autoclass:: llvm2py.ir.instruction.LandingPad
.. autoclass:: llvm2py.ir.instruction.CatchPad
.. autoclass:: llvm2py.ir.instruction.CleanupPad
