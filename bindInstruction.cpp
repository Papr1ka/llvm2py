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
#include "ValueWrapper.h"

namespace py = pybind11;
using namespace llvm;

namespace llvm_python {

    void init_instruction(py::module_ &m) {
        py::class_<InstructionWrapper> instructionObject(m, "Instruction");
        instructionObject.def("__str__", [](InstructionWrapper *instruction) {
            return toString<InstructionWrapper>(instruction, "Instruction");
        });

        instructionObject.def("getOperand", [](InstructionWrapper* instruction, unsigned int i)
        {
            return (ValueWrapper*) instruction->getOperand(i);
        }, py::return_value_policy::reference);

        instructionObject.def("getValue", [](InstructionWrapper* instruction)
        {
            std::string container;
            llvm::raw_string_ostream OS(container);
//            instruction->print(OS);
            return "<llvm_python.Instruction '" + instruction->getNameOrAsOperand() + "'>\n" + OS.str();
        });
    }
}