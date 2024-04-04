#include <pybind11/pybind11.h>
#include "../include/parser.h"
#include "../include/module.h"

namespace py = pybind11;

namespace llvm_python {

    PYBIND11_MODULE(_llvm_python, m) {
        m.doc() = "Python & LLVM IR parser, an early beginning...";
        m.def("parse_assembly", &llvm_python::createModule);
    }
}