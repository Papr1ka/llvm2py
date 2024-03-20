//
// Created by joe on 20.03.24.
//

#ifndef LLVM_PYTHON_INSTRUCTIONWRAPPER_H
#define LLVM_PYTHON_INSTRUCTIONWRAPPER_H
#include "llvm/IR/Instruction.h"

class InstructionWrapper : public llvm::Instruction
{
public:
    ~InstructionWrapper() {};
};

#endif //LLVM_PYTHON_INSTRUCTIONWRAPPER_H
