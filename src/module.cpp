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
        py::object GlobalVariablePyClass;
        py::object ArgumentPyClass;
        py::object TypePyClass;
        py::object ValuePyClass;
        py::object InstructionPyClass;
    };

    py::object handleType(Type *type, const PythonTypes &PT)
    {
        py::dict data;
        if (type->isArrayTy())
        {
            data["num_elements"] = py::int_(type->getArrayNumElements());
            for (auto& i : type->subtypes())
            {
                data["subtype"] = handleType(i, PT);
            }
        }
        return PT.TypePyClass(
                py::cast(to_string<Type>(type)),
                py::cast((int) type->getTypeID()),
                data
        );
    }

    py::object handleOperand(Value *value, const PythonTypes &PT)
    {
        if (auto * constExpr = dyn_cast<ConstantExpr>(value))
        {
            Instruction* instr = constExpr->getAsInstruction();
            return handleInstruction(*instr, PT);
        }
        py::object valueObject = PT.ValuePyClass(
                py::str(getNameOrAsOperand(value)),
                handleType(value->getType(), PT),
                py::cast(to_string(value))
                );
        return valueObject;
    }

    py::object handleGlobalObjectToTuple(const GlobalObject& globalObject, const PythonTypes& PT)
    {
        MaybeAlign Align = globalObject.getAlign();
        int alignment = Align ? Align->value() : 0;
        return py::make_tuple(
            py::int_((int ) globalObject.getAddressSpace()),
            py::int_(alignment),
            py::int_((int ) globalObject.getLinkage()),
            py::int_((int) globalObject.getUnnamedAddr()),
            py::int_((int) globalObject.getVisibility())
        );
    }

    py::object handleValueToTuple(const Value& value, const PythonTypes& PT)
    {
        return py::make_tuple(
                py::str(getNameOrAsOperand(value)),
                handleType(value.getType(), PT),
                py::cast(to_string(&value))
        );
    }

    py::object handleInstructionSpecific(Instruction& instruction, const PythonTypes &PT)
    {
        py::dict data;
        if (auto * instr = dyn_cast<AllocaInst>(&instruction))
        {
            data["AllocatedType"] = handleType(instr->getAllocatedType(), PT);
            data["Align"] = py::int_(instr->getAlign().value());
        }
        else if (auto * instr = dyn_cast<GetElementPtrInst>(&instruction))
        {
            data["SourceElementType"] = handleType(instr->getSourceElementType(), PT);
            data["ResultElementType"] = handleType(instr->getResultElementType(), PT);
            std::vector<py::object> indices;

            for (auto &i : instr->indices())
            {
                indices.push_back(handleValueToTuple(*i.get(), PT));
            }
            data["Indices"] = py::tuple(py::cast(indices));
        }
        else if (auto * instr = dyn_cast<PHINode>(&instruction))
        {
            std::vector<py::object> incomingBlocks;
            for (const BasicBlock* block : instr->blocks())
            {
                incomingBlocks.push_back(py::str(getNameOrAsOperand(block)));
            }
            data["IncomingBlocks"] = py::tuple(py::cast(incomingBlocks));
        }
        return data;
    }

    py::object handleInstruction(Instruction &instruction, const PythonTypes &PT)
    {
        std::vector<py::object> operands;

        py::object data = handleInstructionSpecific(instruction, PT);

        for (Use& operand : instruction.operands())
        {
            py::object operandObject = handleOperand(operand.get(), PT);
            operands.push_back(operandObject);
        }

        py::object instructionObject = PT.InstructionPyClass(
                py::cast(instruction.getOpcode()),
                py::str(instruction.getOpcodeName()),
                py::tuple(py::cast(operands)),
                data,
                handleValueToTuple(instruction, PT)
                );
        return instructionObject;
    }

    py::object handleBlock(BasicBlock &block, const PythonTypes &PT)
    {
        std::vector<py::object> instructions;
        std::vector<py::object> predBlocks;

        instructions.reserve(block.size());

        for (BasicBlock* basicBlock : predecessors(&block))
        {
            predBlocks.push_back(py::str(getNameOrAsOperand(basicBlock)));
        }

        for (Instruction &instruction: block) {
            py::object instructionObject = handleInstruction(instruction, PT);
            instructions.push_back(instructionObject);
        }

        py::object blockObject = PT.BlockPyClass(
                py::tuple(py::cast(instructions)),
                py::tuple(py::cast(predBlocks)),
                handleValueToTuple(block, PT)
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
            initializer = handleValueToTuple(*var.getInitializer(), PT); 
        }
        else
        {
            initializer = py::none();
        }

        py::object globalVariableObject = PT.GlobalVariablePyClass(
            py::tuple(py::cast(attributes)),
            initializer,
            py::bool_(var.isConstant()),
            py::bool_(var.isExternallyInitialized()),
            handleGlobalObjectToTuple(var, PT),
            handleValueToTuple(var, PT)
            );
        return globalVariableObject;
    }

    py::object handleArgument(Argument &argument, const PythonTypes &PT)
    {
        py::object argumentObject = PT.ArgumentPyClass(
                py::int_(argument.getArgNo()),
                handleValueToTuple(argument, PT)
                );
        return argumentObject;
    }

    py::object handleFunction(Function &function, const PythonTypes &PT)
    {
        std::vector<py::object> args;

        for (Argument &arg: function.args())
        {
            py::object argumentObject = handleArgument(arg, PT);
            args.push_back(argumentObject);
        }

        std::vector<py::object> blocks;

        for (BasicBlock &block: function)
        {
            blocks.push_back(handleBlock(block, PT));
        }

        std::vector<py::object> attributeList;

        for (const AttributeSet &attributeSet: function.getAttributes())
        {
            std::vector<py::object> attributes;
            attributes.reserve(attributeSet.getNumAttributes());

            for (const Attribute &attribute: attributeSet)
            {
                py::object attributeObject = py::str(attribute.getAsString());
                attributes.push_back(attributeObject);
            }
            attributeList.push_back(py::tuple(py::cast(attributes)));
        }

        py::object functionObject = PT.FunctionPyClass(
                py::tuple(py::cast(args)),
                py::tuple(py::cast(blocks)),
                py::tuple(py::cast(attributeList)),
                handleType(function.getReturnType(), PT),
                py::int_((int )function.getCallingConv()),
                handleGlobalObjectToTuple(function, PT),
                handleValueToTuple(function, PT)
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

        for (Function &function: *module)
        {
            functions.push_back(handleFunction(function, PT));
        }

        py::object moduleObject = PT.ModulePyClass(
                py::tuple(py::cast(functions)),
                py::tuple(py::cast(globalVariables)),
                py::cast(to_string(module))
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
                IRPyModule.attr("GlobalVariable"),
                IRPyModule.attr("Argument"),
                IRPyModule.attr("Type"),
                IRPyModule.attr("Value"),
                IRPyModule.attr("Instruction"),
        };

        std::unique_ptr<Module> module = parse_module(IR);
        py::object result = handleModule(module.get(), PT);
        return result;
    }
}
