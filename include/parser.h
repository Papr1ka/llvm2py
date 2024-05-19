//
// Created by joe on 24.03.24.
//

#ifndef LLVM2PY_PARSER_H
#define LLVM2PY_PARSER_H

#include "llvm/IRReader/IRReader.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/SourceMgr.h"
#include "llvm/IR/Module.h"

using namespace llvm;

namespace llvm2py
{
    std::unique_ptr<Module> parse_module(const std::string& irPresentation);
}

#endif //LLVM2PY_PARSER_H
