//
// Created by joe on 24.03.24.
//

#ifndef LLVM_PYTHON_PARSER_H
#define LLVM_PYTHON_PARSER_H

#include "llvm/IRReader/IRReader.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/SourceMgr.h"
#include "llvm/IR/Module.h"

using namespace llvm;

namespace llvm_python
{
    Module* parse_module(const std::string& irPresentation);
}

#endif //LLVM_PYTHON_PARSER_H
