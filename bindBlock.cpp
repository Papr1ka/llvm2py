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
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace llvm;

namespace llvm_python {

    void init_block(py::module_ &m) {
        py::class_<BasicBlock> blockObject(m, "Block");

        blockObject.def("__str__", [](BasicBlock *block) {
            return toString<BasicBlock>(block, "Block");
        });

        blockObject.def("getInstructions", [](BasicBlock* block)
        {
            std::vector<InstructionWrapper *> instructions;
            for (Instruction& instruction : *block)
            {
                instructions.push_back((InstructionWrapper*) &instruction);
                instruction.operands();
            }
            return instructions;
        }, py::return_value_policy::reference);
    }
}