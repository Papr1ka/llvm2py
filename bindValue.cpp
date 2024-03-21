//
// Created by joe on 20.03.24.
//
//
// Created by joe on 20.03.24.
//

#include "llvm/IR/Module.h"
#include "tools.h"
#include "ValueWrapper.h"
#include <pybind11/pybind11.h>
#include "InstructionWrapper.h"

namespace py = pybind11;
using namespace llvm;

namespace llvm_python {

    void init_value(py::module_ &m) {
        py::class_<ValueWrapper> valueObject(m, "Value");

        valueObject.def("__str__", [](ValueWrapper* value)
        {
            std::string container;
            std::string container2;
            llvm::raw_string_ostream OS(container);
            llvm::raw_string_ostream OS2(container2);
            value->print(OS);
//            value->getType()->getScalarType()->print(OS2);
            value->getType()->print(OS2);
            return "<llvm_python.Value named '" + value->getNameOrAsOperand() +
            "' type '" + OS2.str() + "'"+ "'>\n" + OS.str();
        });
    }
}