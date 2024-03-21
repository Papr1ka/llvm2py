//
// Created by joe on 20.03.24.
//

#include "llvm/IR/Module.h"
#include "tools.h"
#include <pybind11/pybind11.h>
#include <iostream>

namespace py = pybind11;
using namespace llvm;

namespace llvm_python {

    py::typing::Iterator<BasicBlock> moduleIterable(Function *function) {
        auto blockIterator = function->getIterator();
        return py::make_iterator(blockIterator->begin(), blockIterator->end());
    }

    void init_function(py::module_ &m) {
        py::class_<Function> func(m, "Function");
        func.def_property_readonly("name", [](Function *function) {
            return function->getName().str();
        });
        func.def("__repr__", [](Function *function) {
            return "<llvm_python.Function named '" + function->getName().str() + "'>";
        });
        func.def("__str__", [](Function *function) {
            return toString<Function>(function, "Function");
        });
        func.def_property_readonly("blocks", moduleIterable);
        func.def_property_readonly("args", [](Function *function) {
            return py::make_iterator(function->arg_begin(), function->arg_end());
        });
        func.def_property_readonly("attributes", [](Function* function)
        {
            function->getAttributes()
        })
    }
}