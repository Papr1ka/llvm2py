//
// Created by joe on 20.03.24.
//

#ifndef LLVM_PYTHON_TOOLS_H
#define LLVM_PYTHON_TOOLS_H
#include "string"
#include "llvm/Support/raw_ostream.h"

template <typename T>
std::string toString(T* object, std::string&& name)
{
    std::string container;
    llvm::raw_string_ostream OS(container);
    object->print(OS);
    return "<llvm_python." + name + " named '" + object->getName().str() + "'>\n" + OS.str();
}

#endif //LLVM_PYTHON_TOOLS_H
