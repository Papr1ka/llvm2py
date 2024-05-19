#include <pybind11/pybind11.h>
#include "../include/parser.h"
#include "../include/module.h"

namespace py = pybind11;

namespace llpy {

    PYBIND11_MODULE(_llpy, m) {
        m.doc() = "Python & LLVM IR parser, an early beginning...";
        m.def("parse_assembly", &llpy::createModule);
    }
}