from ast import *
import graphlib


src = """
from typing import NamedTuple


class Instruction(NamedTuple):
    # instruction attributes
    attrs: Attrs

    # instruction as value
    result: Value

    # instruction opcode
    opcode: str


class CallInstr(Instruction):
    call_attributes: list[Attrs]


class Invoke(CallInstr):
    func: Value
    args: list[Value]
    label_ok: Value
    label_err: Value

    def __str__(self):
        return (
            f"{self.result} = invoke {self.func}({', '.join(map(str, self.args))}) "
            + (f"to {self.label_ok} unwind {self.label_err}")
        )

"""

tree = parse(src)
print(dump(tree, indent=4))


def construct_final(class_def: ClassDef, names: dict[str, ClassDef]):
    match class_def:
        case ClassDef(
            name, [Name("NamedTuple")], keywords, body, decorator_list, type_params
        ):
            return class_def
        case ClassDef(name, bases, keywords, body, decorator_list, type_params):
            for base in bases:
                base_class = construct_final(names[base.id], names)
                match base_class:
                    case ClassDef(
                        _,
                        _,
                        base_keywords,
                        base_body,
                        base_decorator_list,
                        base_type_params,
                    ):
                        body = base_body + body
                        decorator_list = base_decorator_list + decorator_list
                        type_params = base_type_params + type_params
                        keywords = base_keywords + keywords
            return ClassDef(
                name, [Name("NamedTuple")], keywords, body, decorator_list, type_params
            )


# def build_graph(mod: Module):
#     match mod:
#         case Module(body):
#             for s in body:
#                 match s:
#                     case ClassDef(name):
#                         names[name] = s
#                         new_class = construct_final(s, names)
#                         new_body.append(new_class)


match tree:
    case Module(body):
        new_body = []
        names = {}
        for s in body:
            match s:
                case ClassDef(name):
                    names[name] = s
                    new_class = construct_final(s, names)
                    new_body.append(new_class)
                case _:
                    new_body.append(s)
        new_mod = Module(new_body, [])
        print(dump(new_mod, indent=4))
        print(unparse(new_mod))
