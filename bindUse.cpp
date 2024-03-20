//
// Created by joe on 20.03.24.
//
//
// Created by joe on 20.03.24.
//

#include "llvm/IR/Module.h"
#include "tools.h"
#include <pybind11/pybind11.h>
#include "InstructionWrapper.h"

namespace py = pybind11;
using namespace llvm;

namespace llvm_python {

    void init_instruction(py::module_ &m) {
        py::class_<Use> useObject(m, "Use");
        instructionObject.def("__str__", [](InstructionWrapper *instruction) {
            return toString<InstructionWrapper>(instruction, "Instruction");
        });

        instructionObject.def("");
    }
}