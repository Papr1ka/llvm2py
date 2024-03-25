#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/ModuleParser.h"
#include "../include/module.h"

namespace py = pybind11;

namespace llvm_python {

    py::object test(const std::string& ir)
    {
        Module* module = parse_module(ir);
        py::object m = py::module_::import("ir");
        py::object q = m.attr("Module");
        q.attr("name") = module->getName().str();
        delete module;
        return q();
    }

    PYBIND11_MODULE(llvm_python, m) {
        m.doc() = "Python & LLVM IR parser, an early beginning...";
        m.def("createModule", &llvm_python::createModule);
        m.def("test", &test);
        py::enum_<Type::TypeID>(m, "Type");
    }
}