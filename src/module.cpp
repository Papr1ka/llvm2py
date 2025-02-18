#include "../include/module.h"
#include "../include/parser.h"
#include "../include/tools.h"
#include <iostream>

namespace llvm2py {

    struct PythonTypes {
        py::object IRPyModule;
        py::object ModulePyClass;
        py::object FunctionPyClass;
        py::object BlockPyClass;
        py::object GlobalObjectPyClass;
        py::object GlobalVariablePyClass;
        py::object ValuePyClass;

        // Types
        py::object VoidTypePyClass;
        py::object FunctionTypePyClass;
        py::object IntegerTypePyClass;
        py::object FPTypePyClass;
        py::object X86_mmxTypePyClass;
        py::object X86_amxTypePyClass;
        py::object PtrTypePyClass;
        py::object TargetExtensionTypePyClass;
        py::object VectorTypePyClass;
        py::object LabelTypePyClass;
        py::object TokenTypePyClass;
        py::object MetadataTypePyClass;
        py::object ArrayTypePyClass;
        py::object StructureTypePyClass;
        py::object OpaqueTypePyClass;

        // Instruction Factory
        py::object createInstructionFactory;
    };

    bool supportsFastMathFlags(unsigned opcode)
    {
        switch (opcode)
        {
        case Instruction::FNeg:
        case Instruction::FAdd:
        case Instruction::FSub:
        case Instruction::FMul:
        case Instruction::FDiv:
        case Instruction::FRem:
        case Instruction::FPTrunc:
        case Instruction::FPExt:
        case Instruction::FCmp:
        case Instruction::PHI:
        case Instruction::Select:
        case Instruction::Call:
            return true;
        default:
            return false;
        }
    }

    bool supportsNUWandNSW(unsigned opcode)
    {
        switch (opcode)
        {
        case Instruction::GetElementPtr:
        case Instruction::Add:
        case Instruction::Sub:
        case Instruction::Mul:
        case Instruction::Shl:
        case Instruction::Trunc:
            return true;
        default:
            return false;
        }
    }

    bool supportsExact(unsigned opcode)
    {
        switch (opcode)
        {
        case Instruction::UDiv:
        case Instruction::SDiv:
        case Instruction::LShr:
        case Instruction::AShr:
            return true;
        default:
            return false;
        }
    }

    py::object handleType(Type *type, const PythonTypes &PT)
    {
        switch (type->getTypeID())
        {
            // Simple types
            case Type::TypeID::HalfTyID:
                return PT.FPTypePyClass(py::str("half"));
            case Type::TypeID::BFloatTyID:
                return PT.FPTypePyClass(py::str("bfloat"));
            case Type::TypeID::FloatTyID:
                return PT.FPTypePyClass(py::str("float"));
            case Type::TypeID::DoubleTyID:
                return PT.FPTypePyClass(py::str("double"));
            case Type::TypeID::X86_FP80TyID:
                return PT.FPTypePyClass(py::str("x86_fp80"));
            case Type::TypeID::FP128TyID:
                return PT.FPTypePyClass(py::str("fp128"));
            case Type::TypeID::PPC_FP128TyID:
                return PT.FPTypePyClass(py::str("ppc_fp128"));
            case Type::TypeID::VoidTyID:
                return PT.VoidTypePyClass();
            case Type::TypeID::LabelTyID:
                return PT.LabelTypePyClass();
            case Type::TypeID::MetadataTyID:
                return PT.MetadataTypePyClass();
            case Type::TypeID::X86_MMXTyID:
                return PT.X86_mmxTypePyClass();
            case Type::TypeID::X86_AMXTyID:
                return PT.X86_amxTypePyClass();
            case Type::TypeID::TokenTyID:
                return PT.TokenTypePyClass();

            // Complex types
            case Type::TypeID::IntegerTyID:
            {
                IntegerType* integerTy = (IntegerType*) type;
                return PT.IntegerTypePyClass(
                    py::int_(integerTy->getBitWidth())
                );
            }
            case Type::TypeID::FunctionTyID:
            {    
                FunctionType* functionTy = (FunctionType*) type;
                std::vector<py::object> params;
                for (Type* paramTy : functionTy->params())
                {
                    params.push_back(handleType(paramTy, PT));
                }
                return PT.FunctionTypePyClass(
                    py::list(py::cast(params)),
                    handleType(functionTy->getReturnType(), PT)
                );
            }
            case Type::TypeID::PointerTyID:
            {
                PointerType* ptrTy = (PointerType*) type;
                return PT.PtrTypePyClass(py::int_(ptrTy->getAddressSpace()), py::none());
            }
            case Type::TypeID::StructTyID:
            {
                StructType* structTy = (StructType*)(type);
                if (structTy->isOpaque())
                {
                    return PT.OpaqueTypePyClass();
                }
                else
                {
                    py::object name;
                    if (structTy->hasName())
                    {
                        name = py::str(structTy->getName().str());
                    }
                    else
                    {
                        name = py::none();
                    }
                    std::vector<py::object> elemTypes;
                    for (Type* elemTy : structTy->elements())
                    {
                        elemTypes.push_back(handleType(elemTy, PT));
                    }
                    return PT.StructureTypePyClass(
                        name,
                        py::list(py::cast(elemTypes)),
                        py::bool_(structTy->isPacked())
                    );
                }
            }
            case Type::TypeID::ArrayTyID:
            {
                ArrayType* arrayTy = (ArrayType*) type;
                return PT.ArrayTypePyClass(
                    py::int_(arrayTy->getNumElements()),
                    handleType(arrayTy->getElementType(), PT)
                );
            }
            case Type::TypeID::FixedVectorTyID:
            {
                FixedVectorType* vectorTy = (FixedVectorType*) type;
                return PT.VectorTypePyClass(
                    py::int_(vectorTy->getNumElements()),
                    handleType(vectorTy->getElementType(), PT),
                    py::bool_(false)
                );
            }
            case Type::TypeID::ScalableVectorTyID:
            {
                ScalableVectorType* vectorTy = (ScalableVectorType*) type;
                return PT.VectorTypePyClass(
                    py::int_(vectorTy->getMinNumElements()),
                    handleType(vectorTy->getElementType(), PT),
                    py::bool_(false)
                );
            }
            case Type::TypeID::TypedPointerTyID:
            {
                TypedPointerType* typedPtrTy = (TypedPointerType*) type;
                return PT.PtrTypePyClass(
                    py::int_(typedPtrTy->getAddressSpace()),
                    handleType(typedPtrTy->getElementType(), PT)
                );
            }
            case Type::TypeID::TargetExtTyID:
            {
                TargetExtType* targetExtType = (TargetExtType*) type;
                std::vector<py::object> params;
                for (Type* paramTy : targetExtType->type_params())
                {
                    params.push_back(handleType(paramTy, PT));
                }

                for (unsigned intParam : targetExtType->int_params())
                {
                    params.push_back(py::int_(intParam));
                }

                return PT.TargetExtensionTypePyClass(
                    py::str(targetExtType->getName().str()),
                    py::list(py::cast(params))
                );
            }
        }
    }

    py::object handleGlobalObject(const GlobalObject& globalObject, const PythonTypes& PT)
    {
        MaybeAlign Align = globalObject.getAlign();
        int alignment = Align ? Align->value() : 0;
        return PT.GlobalObjectPyClass(
            py::int_((int ) globalObject.getAddressSpace()),
            py::int_(alignment),
            py::int_((int ) globalObject.getLinkage()),
            py::int_((int) globalObject.getUnnamedAddr()),
            py::int_((int) globalObject.getVisibility())
        );
    }

    py::object handleValue(const Value& value, const PythonTypes& PT)
    {
        py::object data;
        if (auto* constInt = dyn_cast<ConstantInt>(&value))
        {
            data = py::int_(constInt->getSExtValue());
        }
        else if (auto* constFP = dyn_cast<ConstantFP>(&value))
        {
            data = py::float_(constFP->getValue().convertToDouble());
        }
        else if (dyn_cast<ConstantAggregateZero>(&value))
        {
            data = py::int_(0);
        }
        else if (dyn_cast<ConstantPointerNull>(&value))
        {
            data = py::none();
        }
        else if (auto* seqData = dyn_cast<ConstantDataSequential>(&value))
        {
            if (seqData->isString())
            {
                std::string string = seqData->getAsString().str();
                data = py::bytes(string);
            }
            else if (seqData->getElementType()->isIntegerTy())
            {
                std::vector<py::object> elems;
                elems.reserve(seqData->getNumElements());
                for (unsigned i = 0; i < seqData->getNumElements(); i++)
                {
                    int64_t elem = seqData->getElementAsAPInt(i).getSExtValue();
                    elems.push_back(py::int_(elem));
                }
                data = py::list(py::cast(elems));
            }
            else if (seqData->getElementType()->isFloatingPointTy())
            {
                std::vector<py::object> elems;
                elems.reserve(seqData->getNumElements());
                for (unsigned i = 0; i < seqData->getNumElements(); i++)
                {
                    double elem = seqData->getElementAsDouble(i);
                    elems.push_back(py::float_(elem));
                }
                data = py::list(py::cast(elems));
            }
            else
            {
                std::vector<py::object> elems;
                elems.reserve(seqData->getNumElements());
                for (unsigned i = 0; i < seqData->getNumElements(); i++)
                {
                    Constant* elem = seqData->getElementAsConstant(i);
                    elems.push_back(handleValue(*elem, PT));
                }
                data = py::list(py::cast(elems));
            }
        }
        else if (auto* constAggregate = dyn_cast<ConstantAggregate>(&value))
        {
            std::vector<py::object> elems;
            elems.reserve(constAggregate->getNumOperands());
            for (const Use& operand : constAggregate->operands())
            {
                Value* elem = operand.get();
                elems.push_back(handleValue(*elem, PT));
            }
            data = py::list(py::cast(elems));
        }
        else if (auto* blockAddr = dyn_cast<BlockAddress>(&value))
        {
            data = py::make_tuple(
                py::str(getNameOrAsOperand(blockAddr->getFunction())),
                py::str(getNameOrAsOperand(blockAddr->getBasicBlock()))
            );
        }
        else if (auto* constExpr = dyn_cast<ConstantExpr>(&value))
        {
            Instruction* instr = constExpr->getAsInstruction();
            data = handleInstruction(*instr, PT);
        }
        else
        {
            data = py::str(getNameOrAsOperand(value));
        }

        return PT.ValuePyClass(
            data,
            handleType(value.getType(), PT)
        );
    }

    py::object handleInstructionSpecific(const Instruction& instruction, const PythonTypes &PT)
    {
        unsigned opcode = instruction.getOpcode();
        switch (opcode)
        {
            case Instruction::CallBr:
            {
                CallBrInst* instr = (CallBrInst*)(&instruction);
                return py::make_tuple(py::int_(instr->getNumIndirectDests()));
            }
            case Instruction::CatchSwitch:
            {
                CatchSwitchInst* instr = (CatchSwitchInst*)(&instruction);
                return py::make_tuple(py::bool_(instr->hasUnwindDest()));
            }
            case Instruction::ExtractValue:
            {
                ExtractValueInst* instr = (ExtractValueInst*)(&instruction);
                std::vector<py::object> arr;
                ArrayRef indices = instr->getIndices();
                arr.reserve(indices.size());
                for (unsigned i : indices)
                {
                    arr.push_back(py::int_(i));
                }
                return py::make_tuple(py::list(py::cast(arr)));
            }
            case Instruction::InsertValue:
            {
                InsertValueInst* instr = (InsertValueInst*)(&instruction);
                std::vector<py::object> arr;
                ArrayRef indices = instr->getIndices();
                arr.reserve(indices.size());
                for (unsigned i : indices)
                {
                    arr.push_back(py::int_(i));
                }
                return py::make_tuple(py::list(py::cast(arr)));
            }
            case Instruction::Alloca:
            {
                AllocaInst* instr = (AllocaInst*)(&instruction);
                return py::make_tuple(
                    handleType(instr->getAllocatedType(), PT)
                );
            }
            case Instruction::GetElementPtr:
            {
                GetElementPtrInst* instr = (GetElementPtrInst*)(&instruction);
                return py::make_tuple(
                    handleType(instr->getResultElementType(), PT),
                    handleType(instr->getSourceElementType(), PT)
                );
            }
            case Instruction::ICmp:
            case Instruction::FCmp:
            {
                CmpInst* instr = (CmpInst*)(&instruction);
                return py::make_tuple(
                    py::str(instr->getPredicateName(instr->getPredicate()).str())
                );
            }
            case Instruction::PHI:
            {
                PHINode* instr = (PHINode*)(&instruction);
                std::vector<py::object> incomingBlocks;
                for (const BasicBlock* block : instr->blocks())
                {
                    incomingBlocks.push_back(py::str(getNameOrAsOperand(block)));
                }
                return py::make_tuple(py::list(py::cast(incomingBlocks)));
            }
            case Instruction::LandingPad:
            {
                LandingPadInst* instr = (LandingPadInst*)(&instruction);
                std::vector<py::object> arr;
                unsigned numClauses = instr->getNumClauses();
                arr.reserve(numClauses);
                for (unsigned i = 0; i < numClauses; i++)
                {
                    arr.push_back(py::bool_(instr->isCatch(i)));
                }
                return py::make_tuple(
                    py::bool_(instr->isCleanup()),
                    py::list(py::cast(arr))
                );
            }
            case Instruction::AtomicRMW:
            {
                AtomicRMWInst* instr = (AtomicRMWInst*)(&instruction);
                return py::make_tuple(py::str(instr->getOperationName(instr->getOperation()).str()));
            }
            default:
                return py::none();
        }
    }

    void extractFastMathFlags(const Instruction &instruction, std::vector<py::object>* flags)
    {
        if (!supportsFastMathFlags(instruction.getOpcode())) return;

        const FastMathFlags fastFlags = instruction.getFastMathFlags();
        if (fastFlags.allowReassoc()) flags->push_back(py::make_tuple(py::str("reassoc")));
        if (fastFlags.noNaNs()) flags->push_back(py::make_tuple(py::str("nnan")));
        if (fastFlags.noInfs()) flags->push_back(py::make_tuple(py::str("ninf")));
        if (fastFlags.noSignedZeros()) flags->push_back(py::make_tuple(py::str("nsz")));
        if (fastFlags.allowReciprocal()) flags->push_back(py::make_tuple(py::str("recip")));
        if (fastFlags.allowContract()) flags->push_back(py::make_tuple(py::str("contract")));
        if (fastFlags.approxFunc()) flags->push_back(py::make_tuple(py::str("approx-func")));
    }

    py::object extractInstructionFlags(const Instruction &instruction)
    {
        std::vector<py::object> flags;
        extractFastMathFlags(instruction, &flags);
        unsigned opcode = instruction.getOpcode();
        
        if (supportsNUWandNSW(opcode))
        {
            if (opcode == Instruction::GetElementPtr && instruction.hasNoUnsignedWrap() && instruction.hasNoSignedWrap())
            {
                flags.push_back(py::make_tuple(py::str("nusw")));
            }
            else if (instruction.hasNoUnsignedWrap()) flags.push_back(py::make_tuple(py::str("nuw")));
            else if (instruction.hasNoSignedWrap()) flags.push_back(py::make_tuple(py::str("nsw")));
        }
        
        if (supportsExact(opcode) && instruction.isExact()) flags.push_back(py::make_tuple(py::str("exact")));

        if (auto* instr = dyn_cast<LoadInst>(&instruction))
        {
            if (instr->isVolatile()) flags.push_back(py::make_tuple(py::str("volatile")));
            if (instr->isAtomic()) flags.push_back(py::make_tuple(py::str("atomic")));
            
            AtomicOrdering ordering = instr->getOrdering();
            switch (ordering)
            {
            case AtomicOrdering::Unordered:
                flags.push_back(py::make_tuple(py::str("unordered")));
                break;
            case AtomicOrdering::Monotonic:
                flags.push_back(py::make_tuple(py::str("monotonic")));
                break;
            case AtomicOrdering::Acquire:
                flags.push_back(py::make_tuple(py::str("acquire")));
                break;
            case AtomicOrdering::Release:
                flags.push_back(py::make_tuple(py::str("release")));
                break;
            case AtomicOrdering::AcquireRelease:
                flags.push_back(py::make_tuple(py::str("acrelease")));
                break;
            case AtomicOrdering::SequentiallyConsistent:
                flags.push_back(py::make_tuple(py::str("seqconsistent")));
                break;
            default:
                break;
            }
        }
        else if (auto* instr = dyn_cast<StoreInst>(&instruction))
        {
            if (instr->isVolatile()) flags.push_back(py::make_tuple(py::str("volatile")));
            if (instr->isAtomic()) flags.push_back(py::make_tuple(py::str("atomic")));
            AtomicOrdering ordering = instr->getOrdering();
            switch (ordering)
            {
            case AtomicOrdering::Unordered:
                flags.push_back(py::make_tuple(py::str("unordered")));
                break;
            case AtomicOrdering::Monotonic:
                flags.push_back(py::make_tuple(py::str("monotonic")));
                break;
            case AtomicOrdering::Acquire:
                flags.push_back(py::make_tuple(py::str("acquire")));
                break;
            case AtomicOrdering::Release:
                flags.push_back(py::make_tuple(py::str("release")));
                break;
            case AtomicOrdering::AcquireRelease:
                flags.push_back(py::make_tuple(py::str("acrelease")));
                break;
            case AtomicOrdering::SequentiallyConsistent:
                flags.push_back(py::make_tuple(py::str("seqconsistent")));
                break;
            default:
                break;
            }
        }
        
        switch (instruction.getOpcode())
        {
            case Instruction::Load:
            case Instruction::Store:
            {
                // instruction
                uint64_t align = getLoadStoreAlignment((Value*)&instruction).value();
                flags.push_back(py::make_tuple(py::str("align"), py::int_(align)));
            }
            case Instruction::Fence:
            case Instruction::AtomicCmpXchg:
            case Instruction::AtomicRMW:
            {
                std::optional<SyncScope::ID> id = getAtomicSyncScopeID(&instruction);
                if (id.has_value())
                {
                    py::object scope = id.value() ? py::str("System") : py::str("SingleThread");
                    flags.push_back(py::make_tuple(py::str("syncscope"), scope));
                }
                break;
            }
            default:
                break;
        }

        if (auto* instr = dyn_cast<GetElementPtrInst>(&instruction))
        {
            if (instr->isInBounds()) flags.push_back(py::make_tuple(py::str("inbounds")));
        }

        if (auto* instr = dyn_cast<CallInst>(&instruction))
        {
            CallInst::TailCallKind kind = instr->getTailCallKind();
            switch (kind)
            {
            case CallInst::TailCallKind::TCK_None:
                break;
            case CallInst::TailCallKind::TCK_MustTail:
                flags.push_back(py::make_tuple(py::str("musttail")));
                break;
            case CallInst::TailCallKind::TCK_Tail:
                flags.push_back(py::make_tuple(py::str("tail")));
                break;
            case CallInst::TailCallKind::TCK_NoTail:
                flags.push_back(py::make_tuple(py::str("notail")));
                break;
            default:
                break;
            }
        }

        if (auto* instr = dyn_cast<AllocaInst>(&instruction))
        {
            int align = instr->getAlign().value();
            if (align != 0) flags.push_back(py::make_tuple(py::str("align"), py::int_(align)));

            for (const Use& operand : instr->operands())
            {
                Argument* arg = (Argument*) operand.get();
                if (arg->hasInAllocaAttr())
                {
                    flags.push_back(py::make_tuple(py::str("inalloca")));
                    break;
                }
            }
            int addrSpace = instr->getAddressSpace();
            if (addrSpace != 0)
            {
                flags.push_back(py::make_tuple(py::str("addrspace"), py::int_(addrSpace)));
            }
        }
        return py::set(py::cast(flags));
    }

    py::object handleAttributeList(AttributeList attributes, const PythonTypes &PT)
    {
        std::vector<py::object> allAttrs;
        for (const AttributeSet attrs : attributes)
        {
            std::vector<py::object> localAttrs;
            for (const Attribute attr : attrs)
            {
                Attribute::AttrKind kind = attr.getKindAsEnum();
                if (kind == Attribute::AttrKind::VScaleRange)
                {
                    unsigned min = attr.getVScaleRangeMin();
                    std::optional<unsigned> max = attr.getVScaleRangeMax();
                    if (max.has_value())
                    {
                        localAttrs.push_back(py::make_tuple(
                            py::str(attr.getNameFromAttrKind(kind).str()),
                            py::int_(min),
                            py::int_(max.value())
                        ));
                    }
                    else
                    {
                        localAttrs.push_back(py::make_tuple(
                            py::str(attr.getNameFromAttrKind(kind).str()),
                            py::int_(min)
                        ));
                    }
                }
                else if (attr.isEnumAttribute())
                {
                    localAttrs.push_back(py::make_tuple(
                        py::str(attr.getNameFromAttrKind(kind).str())
                    ));
                }
                else if (attr.isIntAttribute())
                {
                    localAttrs.push_back(py::make_tuple(
                        py::str(attr.getNameFromAttrKind(kind).str()),
                        py::int_(attr.getValueAsInt())
                    ));
                }
                else if (attr.isTypeAttribute())
                {
                    localAttrs.push_back(py::make_tuple(
                        py::str(attr.getNameFromAttrKind(kind).str()),
                        handleType(attr.getValueAsType(), PT)
                    ));
                }
                else
                {
                    localAttrs.push_back(py::make_tuple(
                        py::str(attr.getNameFromAttrKind(kind).str()),
                        py::str(attr.getValueAsString().str())
                    ));
                }
            }
            allAttrs.push_back(py::set(py::cast(localAttrs)));
        }
        return py::list(py::cast(allAttrs));
    }

    py::object handleInstruction(const Instruction &instruction, const PythonTypes &PT)
    {
        std::vector<py::object> operands;

        py::object additional = handleInstructionSpecific(instruction, PT);

        for (const Use& operand : instruction.operands())
        {
            py::object operandObject = handleValue(*operand.get(), PT);
            operands.push_back(operandObject);
        }

        py::object flags = extractInstructionFlags(instruction);

        py::object callBaseAttrs;
        if (auto* instr = dyn_cast<CallBase>(&instruction))
        {
            callBaseAttrs = handleAttributeList(instr->getAttributes(), PT);
        }
        else
        {
            callBaseAttrs = py::none();
        }

        return PT.createInstructionFactory(
                py::int_(instruction.getOpcode()),
                py::str(instruction.getOpcodeName()),
                py::list(py::cast(operands)),
                additional,
                flags,
                callBaseAttrs,
                handleValue(instruction, PT)
            );
    }

    py::object handleBlock(const BasicBlock &block, const PythonTypes &PT)
    {
        std::vector<py::object> instructions;
        std::vector<py::object> predBlocks;

        instructions.reserve(block.size());

        for (const BasicBlock* basicBlock : predecessors(&block))
        {
            predBlocks.push_back(py::str(getNameOrAsOperand(basicBlock)));
        }

        for (const Instruction &instruction: block) {
            py::object instructionObject = handleInstruction(instruction, PT);
            instructions.push_back(instructionObject);
        }

        py::object blockObject = PT.BlockPyClass(
                handleValue(block, PT),
                py::list(py::cast(instructions)),
                py::list(py::cast(predBlocks))
            );
        return blockObject;
    }

    py::object handleGlobalVariable(const GlobalVariable& var, const PythonTypes &PT)
    {
        std::vector<py::object> attributes;
        AttributeSet attributeSet = var.getAttributes();
        attributes.reserve(attributeSet.getNumAttributes());

        for (const Attribute &attribute: attributeSet)
        {
            py::object attributeObject = py::str(attribute.getAsString());
            attributes.push_back(attributeObject);
        }

        py::object initializer;
        if (var.hasInitializer())
        {
            initializer = handleValue(*var.getInitializer(), PT); 
        }
        else
        {
            initializer = py::none();
        }

        return PT.GlobalVariablePyClass(
            handleValue(var, PT),
            initializer,
            py::bool_(var.isConstant()),
            py::list(py::cast(attributes)),
            handleGlobalObject(var, PT),
            py::bool_(var.isExternallyInitialized())
            );
    }

    py::object handleFunction(const Function &function, const PythonTypes &PT)
    {
        std::vector<py::object> args;

        for (const Argument& arg: function.args())
        {
            py::object argumentObject = handleValue(arg, PT);
            args.push_back(argumentObject);
        }

        std::vector<py::object> blocks;

        for (const BasicBlock &block: function)
        {
            blocks.push_back(handleBlock(block, PT));
        }

        py::object attributes = handleAttributeList(function.getAttributes(), PT);

        py::object functionObject = PT.FunctionPyClass(
                handleValue(function, PT),
                py::list(py::cast(args)),
                py::list(py::cast(blocks)),
                attributes,
                py::int_((int )function.getCallingConv()),
                handleGlobalObject(function, PT)
            );
        return functionObject;
    }

    py::object handleModule(Module *module, const PythonTypes &PT)
    {
        std::vector<py::object> functions;
        functions.reserve(module->size());

        std::vector<py::object> globalVariables;
        globalVariables.reserve(module->global_size());

        for (const GlobalVariable& var : module->globals())
        {
            py::object varObject = handleGlobalVariable(var, PT);
            globalVariables.push_back(varObject);
        }

        for (const Function &function: *module)
        {
            functions.push_back(handleFunction(function, PT));
        }

        py::object moduleObject = PT.ModulePyClass(
                py::list(py::cast(functions)),
                py::list(py::cast(globalVariables))
                );
        return moduleObject;
    }

    py::object createModule(const std::string &IR)
    {
        py::object IRPyModule = py::module_::import("llvm2py.ir");
        PythonTypes PT = PythonTypes{
                IRPyModule,
                IRPyModule.attr("Module"),
                IRPyModule.attr("Function"),
                IRPyModule.attr("Block"),
                IRPyModule.attr("GlobalObject"),
                IRPyModule.attr("GlobalVariable"),
                IRPyModule.attr("Value"),
                // types
                IRPyModule.attr("VoidType"),
                IRPyModule.attr("FunctionType"),
                IRPyModule.attr("IntegerType"),
                IRPyModule.attr("FPType"),
                IRPyModule.attr("X86_mmxType"),
                IRPyModule.attr("X86_amxType"),
                IRPyModule.attr("PtrType"),
                IRPyModule.attr("TargetExtensionType"),
                IRPyModule.attr("VectorType"),
                IRPyModule.attr("LabelType"),
                IRPyModule.attr("TokenType"),
                IRPyModule.attr("MetadataType"),
                IRPyModule.attr("ArrayType"),
                IRPyModule.attr("StructureType"),
                IRPyModule.attr("OpaqueType"),

                // Instruction Factory
                IRPyModule.attr("_create_instruction"),
        };

        std::unique_ptr<Module> module = parse_module(IR);
        py::object result = handleModule(module.get(), PT);
        return result;
    }
}
