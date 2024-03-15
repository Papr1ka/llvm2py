#include "llvm/IRReader/IRReader.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/SourceMgr.h"
#include <vector>
#include <pybind11/stl.h>

using namespace llvm;

namespace llvm_python
{
    std::vector<std::string> parseModuleFunctions(std::string irPresentation)
    {
        SMDiagnostic Err;
        LLVMContext Ctx;
        StringRef moduleIR = irPresentation;
        std::unique_ptr<MemoryBuffer> moduleIRBuffer = MemoryBuffer::getMemBuffer(moduleIR, "test", false);
        std::unique_ptr<Module> M = parseIR(*moduleIRBuffer, Err, Ctx);
        
        std::vector<std::string> result;

        M->getFunctionList();

        for (Function &F : *M)
        {
            result.push_back(F.getName().str());
        }
        return result;
    }
}
