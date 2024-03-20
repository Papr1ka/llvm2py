//
// Created by joe on 20.03.24.
//

#ifndef LLVM_PYTHON_VALUEWRAPPER_H
#define LLVM_PYTHON_VALUEWRAPPER_H

#include "llvm/IR/Value.h"

class ValueWrapper : public llvm::Value
{
public:
    ~ValueWrapper() {};
};

#endif //LLVM_PYTHON_VALUEWRAPPER_H
