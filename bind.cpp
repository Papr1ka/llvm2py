#include <pybind11/pybind11.h>
#include <iostream>
#include "ModuleParser.cpp"

namespace py = pybind11;

namespace llvm_python {
    void init_module(py::module_ &);

    void init_function(py::module_ &);

    void init_block(py::module_ &);

    void init_argument(py::module_ &);

    void init_instruction(py::module_ &);

    void init_value(py::module_ &);

    PYBIND11_MODULE(llvm_python, m) {
        m.doc() = "Python & LLVM IR parser, an early beginning...";
        m.def("parse_module", &llvm_python::parse_module, py::return_value_policy::reference,
              "Returns the module object of IR", py::arg("llvm_ir"));

        init_value(m);
        init_instruction(m);
        init_argument(m);
        init_block(m);
        init_function(m);
        init_module(m);
    }
}