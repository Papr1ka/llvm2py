import requests

data = {
    "lang": "c++",
    "filterAnsi": "true",
    "labels": "true",
    "compiler": "clang1100",
    "userArguments": "-emit-llvm",
}
unused = "# Compilation provided by Compiler Explorer at https://godbolt.org/"

def get_ir(cpp_code):
    data.update(source=cpp_code)
    r = requests.post(url="https://godbolt.org/api/noscript/compile", data=data)
    llvm_ir = r.text[len(unused) + 1:]
    if llvm_ir.startswith("<Compilation failed>"):
        raise ValueError("invalid cpp code\n" + r.text)
    return llvm_ir
