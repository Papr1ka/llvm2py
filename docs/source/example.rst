Straightforward simple interpretor
##################################

Let's create a simple interpreter of the llvm ir subset to compute the value of the factorial.

.. _source_program:

Source program
==============

Here is the code of the single test program, whick execution we want to support.

.. code-block:: c

    #include "stdio.h"


    int factorial_cycle(int n)
    {
        int result = 1;
        while (n > 0)
        {
            result *= n;
            n -= 1;
        }
        return result;
    }

    int factorial_req(int n)
    {
        if (n == 1)
        {
            return 1;
        }
        return factorial_req(n - 1) * n;
    }

    int main()
    {
        int factorial_cycle_result = factorial_cycle(10);
        int factorial_req_result = factorial_req(10);
        printf("%d\n", factorial_cycle_result);
        printf("%d\n", factorial_req_result);
        return 0;
    }

.. _compiled program:

Compiled program
================

Now let's look at the compiled version without optimizations

.. code-block:: llvm

    @.str = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1


    define dso_local i32 @factorial_cycle(i32 noundef %0) {
    %2 = alloca i32, align 4
    %3 = alloca i32, align 4
    store i32 %0, ptr %2, align 4
    store i32 1, ptr %3, align 4
    br label %4

    4:                                                ; preds = %7, %1
    %5 = load i32, ptr %2, align 4
    %6 = icmp sgt i32 %5, 0
    br i1 %6, label %7, label %13

    7:                                                ; preds = %4
    %8 = load i32, ptr %2, align 4
    %9 = load i32, ptr %3, align 4
    %10 = mul nsw i32 %9, %8
    store i32 %10, ptr %3, align 4
    %11 = load i32, ptr %2, align 4
    %12 = sub nsw i32 %11, 1
    store i32 %12, ptr %2, align 4
    br label %4

    13:                                               ; preds = %4
    %14 = load i32, ptr %3, align 4
    ret i32 %14
    }

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

    define dso_local i32 @main() #0 {
    %1 = alloca i32, align 4
    %2 = alloca i32, align 4
    %3 = alloca i32, align 4
    store i32 0, ptr %1, align 4
    %4 = call i32 @factorial_cycle(i32 noundef 10)
    store i32 %4, ptr %2, align 4
    %5 = call i32 @factorial_req(i32 noundef 10)
    store i32 %5, ptr %3, align 4
    %6 = load i32, ptr %2, align 4
    %7 = call i32 (ptr, ...) @printf(ptr noundef @.str, i32 noundef %6)
    %8 = load i32, ptr %3, align 4
    %9 = call i32 (ptr, ...) @printf(ptr noundef @.str, i32 noundef %8)
    ret i32 0
    }

    declare dso_local i32 @printf(ptr noundef, ...)

.. _full_implementation:

Full implementation
===================

direct realization may look as follows:

.. code-block:: python

    from llvm2py import parse_assembly
    from llvm2py.ir import *


    def first_value_in_dict(mapping: dict):
        return next(iter(mapping.values()))


    class Mem:
        def __init__(self):
            self.stack_frames = []

        def alloca(self):
            addr = len(self.stack_frames[-1])
            self.stack_frames[-1].append(None)
            return addr

        def store(self, value, addr):
            self.stack_frames[-1][addr] = value

        def load(self, addr):
            return self.stack_frames[-1][addr]

        def new_frame(self):
            self.stack_frames.append([])

        def pop_frame(self):
            return self.stack_frames.pop()


    class State(NamedTuple):
        globals: dict
        vars: dict
        mem: Mem


    def interp_value(value: Value, state):
        globals, vars, _ = state
        match value.val:
            case str(name):
                if name in vars:
                    new_value = vars[name]
                else:
                    new_value = globals[name]
                match new_value:
                    case GlobalVariable(_, initializer):
                        return interp_value(initializer, state)
                    case Value():
                        return interp_value(new_value, state)
                    case _:
                        return new_value
            case int(val):
                return val
            case bytes(val):
                return str(val, "utf-8")
            case _:
                raise NotImplementedError()


    def interp_instr(instr: Instruction, state: State):
        _, vars, mem = state
        match instr:
            case Alloca(Value(addr)):
                vars[addr] = mem.alloca()
            case Store(value, Value(addr)):
                val = interp_value(value, state)
                mem.store(val, vars[addr])
            case Load(Value(res), Value(addr)):
                vars[res] = mem.load(vars[addr])
            case ICmp(cond, Value(res), fst, snd):
                arg0 = interp_value(fst, state)
                arg1 = interp_value(snd, state)
                match cond:
                    case "sgt":
                        vars[res] = arg0 > arg1
                    case "eq":
                        vars[res] = arg0 == arg1
                    case _:
                        raise NotImplementedError()

            case BinOp("mul", Value(res), fst, snd):
                arg0 = interp_value(fst, state)
                arg1 = interp_value(snd, state)
                vars[res] = arg0 * arg1
            case BinOp("sub", Value(res), fst, snd):
                arg0 = interp_value(fst, state)
                arg1 = interp_value(snd, state)
                vars[res] = arg0 - arg1
            case Call(Value(res), Value(func), args):
                func = mod.funcs[func]
                arg_vals = [interp_value(arg, state) for arg in args]
                vars[res] = interp_function(func, arg_vals, state)
            case _:
                raise NotImplementedError()


    def interp_tail(instr: Instruction, state: State):
        match instr:
            case Br(None, Value(label)):
                return (label, None)
            case Br(cond, Value(label_false), Value(label_true)):
                cond_val = interp_value(cond, state)
                if cond_val:
                    return (label_true, None)
                else:
                    return (label_false, None)
            case Ret(value):
                val = interp_value(value, state)
                return (None, val)


    def interp_block(block: Block, state: State):
        *instrs, tail = block.instrs
        for instr in instrs:
            interp_instr(instr, state)
        return interp_tail(tail, state)


    external_functions = {"printf": lambda fmt, *args: print(fmt % tuple(args), end="")}


    def interp_external_function(func: Function, args):
        func_name = func.value.val
        if func_name in external_functions:
            return external_functions[func_name](*args)
        else:
            raise NotImplementedError()


    def interp_function(func: Function, args, state):
        globals, _, mem = state
        vars = {}
        new_state = State(globals, vars, mem)

        for param, arg in zip(func.args, args):
            vars[param.val] = arg

        if func.has_no_body():
            return interp_external_function(func, args)

        mem.new_frame()
        blocks = func.blocks
        fst_block = first_value_in_dict(blocks)
        label, value = interp_block(fst_block, new_state)
        while label is not None:
            label, value = interp_block(blocks[label], new_state)

        mem.pop_frame()
        return value


    def interp_module(mod: Module):
        state = State(mod.global_vars, {}, Mem())
        main = mod.funcs["main"]
        return interp_function(main, [], state)


    if __name__ == "__main__":
        with open("../test_files/factorial.ll") as file:
            source = file.read()

        mod = parse_assembly(source)
        interp_module(mod)

.. _explanation:

Explanation
===========


.. _memory_model:

Memory model
------------

Let's add a couple of comments

.. code-block:: python

    class Mem:
        def __init__(self):
            self.stack_frames = []

        def alloca(self):
            addr = len(self.stack_frames[-1])
            self.stack_frames[-1].append(None)
            return addr

        def store(self, value, addr):
            self.stack_frames[-1][addr] = value

        def load(self, addr):
            return self.stack_frames[-1][addr]

        def new_frame(self):
            self.stack_frames.append([])

        def pop_frame(self):
            return self.stack_frames.pop()

This class models operations with stack memory

- alloca returns the address on the stack of the function that is currently being executed.
- load and store in our program work only with addresses obtained using alloca.
- After the function is executed, the stack frame memory is freed.

Summarizing these facts, we can allow to operate only with the last stack frame.

alloca allocates memory on the stack and returns its “address”
load and store work with memory by “address”
new_frame and pop_frame create and delete stack frames, which is useful.

.. _state:

State
-----

.. code-block:: python

    class State(NamedTuple):
        globals: dict
        vars: dict
        mem: Mem

This class is needed to store the program execution state.

.. _module_interpretation:

Module interpretation
---------------------

.. code-block:: python

    def interp_module(mod: Module):
        state = State(mod.global_vars, {}, Mem())
        main = mod.funcs["main"]
        return interp_function(main, [], state)

Code execution starts with the main function.

.. _function_interpretation:

Function interpretation
-----------------------

.. code-block:: python

    def interp_function(func: Function, args, state):
        globals, _, mem = state
        vars = {}
        new_state = State(globals, vars, mem)

        for param, arg in zip(func.args, args):
            vars[param.val] = arg

        if func.has_no_body():
            return interp_external_function(func, args)

        mem.new_frame()
        blocks = func.blocks
        fst_block = first_value_in_dict(blocks)
        label, value = interp_block(fst_block, new_state)
        while label is not None:
            label, value = interp_block(blocks[label], new_state)

        mem.pop_frame()
        return value

Here a new state is created with an empty vars environment

then the arguments passed to the function are added to the environment

Handle the case when the function is not defined, as for example with printf.

If the function is defined, a new stack frame is created and the execution
of basic blocks starts, starting from the first one (first_value_in_dict),
until one of them returns a value using the Ret instruction.

After that, the stack frame is deleted and the value is returned.

.. _block_interpretation:

Block interpretation
---------------------

.. code-block:: python

    def interp_block(block: Block, state: State):
        *instrs, tail = block.instrs
        for instr in instrs:
            interp_instr(instr, state)
        return interp_tail(tail, state)

Since the terminator instruction appears at the end,
the logic for interpreting the basic block is implemented explicitly.

How to understand when a block has finished using the Ret function,
and when the execution should be continued in another block?

.. _tail_interpretation:

Tail interpretation
-------------------

.. code-block:: python

    def interp_tail(instr: Instruction, state: State):
        match instr:
            case Br(None, Value(label)):
                return (label, None)
            case Br(cond, Value(label_false), Value(label_true)):
                cond_val = interp_value(cond, state)
                if cond_val:
                    return (label_true, None)
                else:
                    return (label_false, None)
            case Ret(value):
                val = interp_value(value, state)
                return (None, val)

.. _instruction_interpretation:

Instruction interpretation
--------------------------

.. code-block:: python

    def interp_instr(instr: Instruction, state: State):
        _, vars, mem = state
        match instr:
            case Alloca(Value(addr)):
                vars[addr] = mem.alloca()
            case Store(value, Value(addr)):
                val = interp_value(value, state)
                mem.store(val, vars[addr])
            case Load(Value(res), Value(addr)):
                vars[res] = mem.load(vars[addr])
            case ICmp(cond, Value(res), fst, snd):
                arg0 = interp_value(fst, state)
                arg1 = interp_value(snd, state)
                match cond:
                    case "sgt":
                        vars[res] = arg0 > arg1
                    case "eq":
                        vars[res] = arg0 == arg1
                    case _:
                        raise NotImplementedError()

            case BinOp("mul", Value(res), fst, snd):
                arg0 = interp_value(fst, state)
                arg1 = interp_value(snd, state)
                vars[res] = arg0 * arg1
            case BinOp("sub", Value(res), fst, snd):
                arg0 = interp_value(fst, state)
                arg1 = interp_value(snd, state)
                vars[res] = arg0 - arg1
            case Call(Value(res), Value(func), args):
                func = mod.funcs[func]
                arg_vals = [interp_value(arg, state) for arg in args]
                vars[res] = interp_function(func, arg_vals, state)
            case _:
                raise NotImplementedError()

interp_instr is fairly straightforward.
alloca, store and load use the Mem class interface.
Call supports only direct calls and calls interp_function after preparing arguments.
All instructions store the result of execution in the vars environment.

.. _value_interpretation:

Value interpretation
--------------------

.. code-block:: python

    def interp_value(value: Value, state):
        globals, vars, _ = state
        match value.val:
            case str(name):
                if name in vars:
                    new_value = vars[name]
                else:
                    new_value = globals[name]
                match new_value:
                    case GlobalVariable(_, initializer):
                        return interp_value(initializer, state)
                    case _:
                        return new_value
            case int(val):
                return val
            case bytes(val):
                return str(val, "utf-8")
            case _:
                raise NotImplementedError()

This function is used to get the computed result from Value.
If Value stores a name, the function first checks the local environment (vars) and then the global environment (globals), after which it can recursively call itself to calculate the global variable.

You may notice that with this implementation, global variables cannot be changed, but this is not required for the computation of our program.

.. _summary:

Summary
=======

Thus, we have implemented a factorial interpreter based on the LLVM IR representation.

Of course, this is not the only usage of the library, but this example is intended to illustrate the general principles of working with the library.

It is worth noting that this implementation does not rely on the usual Visitor pattern,
but uses the match case construct, which will allow you to write more declarative programs.
