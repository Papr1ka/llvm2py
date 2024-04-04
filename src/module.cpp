#include "../include/module.h"
#include "../include/parser.h"
#include "../include/tools.h"
#include <iostream>

namespace llvm_python {

    struct PythonTypes {
        py::object IRPyModule;
        py::object ModulePyClass;
        py::object FunctionPyClass;
        py::object BlockPyClass;
        py::object ArgumentPyClass;
        py::object TypePyClass;
        py::object ValuePyClass;
        py::object InstructionPyClass;
    };

    py::object handleType(Type *type, const PythonTypes &PT)
    {
        py::object typeObject = PT.TypePyClass();
        typeObject.attr("setup")(
                py::cast(to_string<Type>(type)),
                py::cast((int) type->getTypeID())
        );
        return typeObject;
    }

    py::object handleOperand(Value *value, const PythonTypes &PT)
    {
        py::object valueObject = PT.ValuePyClass(
                py::str(getNameOrAsOperand(value)),
                handleType(value->getType(), PT),
                py::cast(to_string(value))
                );
        return valueObject;
    }

    py::object handleValueToTuple(const Value& value, const PythonTypes& PT)
    {
        return py::make_tuple(
                py::str(getNameOrAsOperand(value)),
                handleType(value.getType(), PT),
                py::cast(to_string(&value))
        );
    }

    py::object handleInstruction(Instruction &instruction, const PythonTypes &PT)
    {
        std::vector<py::object> operands;

        for (Use& operand : instruction.operands())
        {
            py::object operandObject = handleOperand(operand.get(), PT);
            operands.push_back(operandObject);
        }

        py::object instructionObject = PT.InstructionPyClass(
                py::cast(instruction.getOpcode()),
                py::str(instruction.getOpcodeName()),
                py::tuple(py::cast(operands)),
                handleValueToTuple(instruction, PT)
                );
        return instructionObject;
    }

    py::object handleBlock(BasicBlock &block, const PythonTypes &PT)
    {
        std::vector<py::object> instructions;

        for (Instruction &instruction: block) {
            py::object instructionObject = handleInstruction(instruction, PT);
            instructions.push_back(instructionObject);
        }

        py::object blockObject = PT.BlockPyClass(
                py::tuple(py::cast(instructions)),
                handleValueToTuple(block, PT)
                );
        return blockObject;
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
                py::int_((int )function.getVisibility()),
                py::int_((int )function.getLinkage()),
                py::int_((int )function.getCallingConv()),
                handleValueToTuple(function, PT)
                );
        return functionObject;
    }

    py::object handleModule(Module *module, const PythonTypes &PT)
    {
        std::vector<py::object> functions;
        functions.reserve(module->size());

        for (Function &function: *module)
        {
            functions.push_back(handleFunction(function, PT));
        }

        py::object moduleObject = PT.ModulePyClass(
                py::tuple(py::cast(functions)),
                py::cast(to_string(module))
                );
        return moduleObject;
    }

    py::object createModule(const std::string &IR)
    {
        py::object IRPyModule = py::module_::import("llvm_python.ir");
        PythonTypes PT = PythonTypes{
                IRPyModule,
                IRPyModule.attr("Module"),
                IRPyModule.attr("Function"),
                IRPyModule.attr("Block"),
                IRPyModule.attr("Argument"),
                IRPyModule.attr("Type"),
                IRPyModule.attr("Value"),
                IRPyModule.attr("Instruction"),
        };

        Module *module = parse_module(IR);
        py::object result = handleModule(module, PT);
        delete module;
        return result;
    }
}
