//
// Created by joe on 24.03.24.
//

#ifndef LLVM_PYTHON_MODULE_H
#define LLVM_PYTHON_MODULE_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Instructions.h"


namespace py = pybind11;
using namespace llvm;

namespace llvm_python {
    py::object createModule(const std::string& IR);
}

#endif //LLVM_PYTHON_MODULE_H
