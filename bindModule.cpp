//
// Created by joe on 20.03.24.
//
#include "llvm/IR/Module.h"
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>

namespace py = pybind11;
using namespace llvm;

namespace llvm_python {

    py::typing::Iterator<Function> moduleIterable(Module *module) {
        SymbolTableList<Function> &functionList = module->getFunctionList();
        return py::make_iterator(functionList.begin(), functionList.end());
    }

    void init_module(py::module_ &m) {
        py::class_<Module> moduleObject(m, "Module");
        moduleObject.def_property_readonly("name", [](Module *module) {
            return module->getName().str();
        });

        moduleObject.def("get_functions", [](Module *module) {
            std::vector<Function *> functions;
            SymbolTableList<Function> &functionList = module->getFunctionList();
            int size = functionList.size();
            functions.reserve(size);
            for (Function &function: module->getFunctionList()) {
                functions.push_back(&function);
            }
            return functions;
        }, py::return_value_policy::reference);

        moduleObject.def_property_readonly("functions", &moduleIterable, py::keep_alive<0, 1>());

        moduleObject.def("__iter__", &moduleIterable, py::keep_alive<0, 1>());

        moduleObject.def("get_function", [](Module *module, const std::string &name) {
            Function *function = module->getFunction(name);
            if (function == nullptr) {
                return py::cast<py::object>(py::none());
            }
            return py::cast(function);
        }, py::arg("function_name"));
    }
}