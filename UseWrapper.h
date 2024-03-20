//
// Created by joe on 20.03.24.
//

#ifndef LLVM_PYTHON_USEWRAPPER_H
#define LLVM_PYTHON_USEWRAPPER_H

#include "llvm/IR/Use.h"

using namespace llvm;

class UseWrapper : public Use
{
public:
    ~UseWrapper() {};
};

#endif //LLVM_PYTHON_USEWRAPPER_H
