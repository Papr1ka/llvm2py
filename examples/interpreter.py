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
