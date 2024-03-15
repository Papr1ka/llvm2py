#include <pybind11/pybind11.h>
#include "ModuleFunctionsParser.cpp"

namespace py = pybind11;

PYBIND11_MODULE(llvm_python, m)
{
    m.doc() = "Python & LLVM IR parser, an early beginning...";
    m.def("parseModuleFunctions", &llvm_python::parseModuleFunctions, "Returns the list of module function names");
}
