#include "../include/parser.h"

namespace llvm2py
{

    static LLVMContext ctx;
    std::unique_ptr<Module> parse_module(const std::string& irPresentation)
    {
        SMDiagnostic Err;
        StringRef moduleIR = irPresentation;
        std::unique_ptr<MemoryBuffer> moduleIRBuffer = MemoryBuffer::getMemBuffer(moduleIR);
        std::unique_ptr<Module> M = parseIR(*moduleIRBuffer, Err, ctx);
        if (!M)
        {
            std::string rw = "Error reading IR file\n";
            llvm::raw_string_ostream OS(rw);
            Err.print(irPresentation.c_str(), OS);
            throw std::invalid_argument(OS.str());
        }
        return M;
    }
}
