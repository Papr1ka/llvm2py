//
// Created by joe on 20.03.24.
//
//
// Created by joe on 20.03.24.
//

#include "llvm/IR/Module.h"
#include "tools.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace llvm;

namespace llvm_python {

    void init_argument(py::module_ &m) {
        py::class_<Argument> argObject(m, "Argument");
        argObject.def("__str__", [](Argument *arg) {
            std::string container;
            llvm::raw_string_ostream OS(container);
            arg->print(OS);
            return "<llvm_python.Argument at pos " + std::to_string(arg->getArgNo()) + ">\n" + OS.str();
        });
    }
}