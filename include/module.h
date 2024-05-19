//
// Created by joe on 24.03.24.
//

#ifndef LLVM2PY_MODULE_H
#define LLVM2PY_MODULE_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/InstrTypes.h"

namespace py = pybind11;
using namespace llvm;

namespace llvm2py {
    py::object createModule(const std::string& IR);
}

#endif //LLVM2PY_MODULE_H
