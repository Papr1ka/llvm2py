#include "llvm/IRReader/IRReader.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/SourceMgr.h"
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace llvm;

namespace llvm_python
{
    static LLVMContext context;

    Module* parse_module(const std::string& irPresentation)
    {
        SMDiagnostic Err;
        StringRef moduleIR = irPresentation;
        std::unique_ptr<MemoryBuffer> moduleIRBuffer = MemoryBuffer::getMemBuffer(moduleIR);
        std::unique_ptr<Module> M = parseIR(*moduleIRBuffer, Err, context);
        if (!M)
        {
            std::string rw = "Error reading IR file\n";
            llvm::raw_string_ostream OS(rw);
            Err.print(irPresentation.c_str(), OS);
            throw std::invalid_argument(OS.str());
        }
        Module* ptr = M.release();
        return ptr;
    }

    void printFunctions(Module* module)
    {
        std::cout << module << std::endl;
        for (Function& function : *module)
        {
            std::cout << function.getName().str() << std::endl;
        }
    }
}
