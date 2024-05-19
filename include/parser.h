//
// Created by joe on 24.03.24.
//

#ifndef LLPY_PARSER_H
#define LLPY_PARSER_H

#include "llvm/IRReader/IRReader.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/SourceMgr.h"
#include "llvm/IR/Module.h"

using namespace llvm;

namespace llpy
{
    std::unique_ptr<Module> parse_module(const std::string& irPresentation);
}

#endif //LLPY_PARSER_H
