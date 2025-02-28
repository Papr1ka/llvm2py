from llvm2py import parse_assembly
from llvm2py.ir import *
from llvm2py.ir.global_object import LinkageType
from llvm2py.ir.instruction import Alloca

with open("./fact.ll") as file:
    source = file.read()

mod = parse_assembly(source)


def has_no_body(func: Function):
    return len(func.blocks) == 0


class Mem:
    def __init__(self):
        self.stack_frames = []

    def alloca(self):
        frame_idx = len(self.stack_frames) - 1
        self.stack_frames[frame_idx].append(None)
        frame_addr = len(self.stack_frames[-1]) - 1
        return (frame_idx, frame_addr)

    def store(self, value, frame_idx, frame_addr):
        self.stack_frames[frame_idx][frame_addr] = value

    def load(self, frame_idx, frame_addr):
        return self.stack_frames[frame_idx][frame_addr]

    def new_frame(self):
        self.stack_frames.append([])

    def pop_frame(self):
        return self.stack_frames.pop()


class State(NamedTuple):
    globals: dict[str, Any]
    vars: dict[str, Any]
    mem: Mem


def find(vars, globals, name):
    for scope in (globals, vars):
        if name in scope:
            return scope[name]
    raise RuntimeError(f"Can't find var with name {name}")


def first_in_dict(mapping: dict):
    return next(iter(mapping.values()))


def interp_value(value, state):
    globals, vars, _ = state
    match value.val:
        case str(name):
            if name in vars:
                value = vars[name]
            else:
                value = globals[name]

            match value:
                case GlobalVariable(_, initializer):
                    return interp_value(initializer, state)
                case Value():
                    return interp_value(value, state)
                case _:
                    return value
        case int(val):
            return val
        case bytes(val):
            return str(val, "utf-8")
        case _:
            raise NotImplementedError()


def interp_instr(instr: Instruction, state: State):
    globals, vars, mem = state
    match instr:
        case Alloca(attrs, Value(res)):
            vars[res] = mem.alloca()
        case Store(attrs, res, _, value, Value(addr)):
            value = interp_value(value, state)
            mem.store(value, *vars[addr])
        case Load(attrs, Value(res), _, Value(addr)):
            vars[res] = mem.load(*vars[addr])
        case ICmp(attrs, Value(res), _, cond, arg0, arg1):
            arg0 = interp_value(arg0, state)
            arg1 = interp_value(arg1, state)
            match cond:
                case "sgt":
                    vars[res] = arg0 > arg1
                case "eq":
                    vars[res] = arg0 == arg1
                case _:
                    raise NotImplementedError()

        case BinOp(attrs, Value(res), "mul", arg0, arg1):
            arg0 = interp_value(arg0, state)
            arg1 = interp_value(arg1, state)
            vars[res] = arg0 * arg1
        case BinOp(attrs, Value(res), "sub", arg0, arg1):
            arg0 = interp_value(arg0, state)
            arg1 = interp_value(arg1, state)
            vars[res] = arg0 - arg1
        case Call(attrs, Value(res), _, _, Value(func), args):
            func = mod.get_function(func)
            args = [interp_value(arg, state) for arg in args]
            vars[res] = interp_function(func, args, state)
        case _:
            raise NotImplementedError()


def interp_tail(instr: Instruction, state: State):
    globals, vars, mem = state
    match instr:
        case Br(attrs, res, _, None, Value(label)):
            return (label, None)
        case Br(attrs, res, _, cond, Value(label_false), Value(label_true)):
            cond = interp_value(cond, state)
            if cond:
                return (label_true, None)
            else:
                return (label_false, None)
        case Ret(attrs, res, _, arg):
            arg = interp_value(arg, state)
            return (None, arg)


def interp_block(block: Block, state: State):
    *instrs, tail = block.instrs
    for instr in instrs:
        interp_instr(instr, state)

    return interp_tail(tail, state)


external_functions = {"printf": lambda fmt, *args: print(fmt % tuple(args), end="")}


def interp_external_function(func: Function, args):
    func_name = func.value.val
    if func_name in external_functions:
        external_functions[func_name](*args)
    else:
        raise NotImplementedError()


def interp_function(func: Function, args, state):
    globals, _, mem = state
    vars = {}
    new_state = State(globals, vars, mem)

    for param, arg in zip(func.args, args):
        vars[param.val] = arg

    if has_no_body(func):
        interp_external_function(func, args)
        return

    mem.new_frame()
    blocks = func.blocks
    fst_block = first_in_dict(blocks)
    label, value = interp_block(fst_block, new_state)
    while value is None:
        label, value = interp_block(blocks[label], new_state)

    # deleting stack frame and scope
    mem.pop_frame()
    return value


def interp_module(mod: Module):
    # new state with globals and empty mem
    state = State(mod.global_vars, {}, Mem())
    main = mod.get_function("main")
    interp_function(main, [], state)


interp_module(mod)
