//
// Created by joe on 26.03.24.
//

#ifndef LLVM2PY_TOOLS_H
#define LLVM2PY_TOOLS_H

#include "llvm/Support/raw_ostream.h"
#include <string>
#include <llvm/IR/Module.h>
#include <llvm/Support/raw_os_ostream.h>

namespace llvm2py
{
    std::string to_string(llvm::Module* object)
    {
        std::string buffer;
        llvm::raw_string_ostream OS(buffer);
        object->print(OS, nullptr);
        return buffer;
    }

    template <typename T>
    std::string to_string(T* object)
    {
        std::string buffer;
        llvm::raw_string_ostream OS(buffer);
        object->print(OS);
        return buffer;
    }

    std::string getNameOrAsOperand(const llvm::Value* object)
    {
        if (!object->getName().empty())
            return std::string(object->getName());

        std::string BBName;
        raw_string_ostream OS(BBName);
        object->printAsOperand(OS, false);
        return OS.str();
    }

    std::string getNameOrAsOperand(const llvm::Value& object)
    {
        if (!object.getName().empty())
            return std::string(object.getName());

        std::string BBName;
        raw_string_ostream OS(BBName);
        object.printAsOperand(OS, false);
        return OS.str();
    }
}

#endif //LLVM2PY_TOOLS_H
