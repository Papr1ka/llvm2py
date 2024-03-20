import llvm_python # Наша C++ библиотека

print(llvm_python.__doc__)

"""
код на c++, который будет переведён в представление llvm_ir
"""

cpp_code1 = """#include <iostream>

int factorial(int n)
{
    int result = 1;
    while (n > 0)
    {
        result *= n;
        n--;
    }
    return result;
}

int fact_req(int n)
{
    if (n == 0)
    {
        return 1;
    }
    return n * fact_req(n - 1);
}

int main()
{
    int r = factorial(12);
    int r2 = fact_req(13);
    std::cout << r << std::endl;
    return 0;
}
"""

cpp_code2 = """#include <iostream>
using namespace std;

int main() {
    int n, t1 = 0, t2 = 1, nextTerm = 0;

    cout << "Enter the number of terms: ";
    cin >> n;

    cout << "Fibonacci Series: ";

    for (int i = 1; i <= n; ++i) {
        // Prints the first two terms.
        if(i == 1) {
            cout << t1 << ", ";
            continue;
        }
        if(i == 2) {
            cout << t2 << ", ";
            continue;
        }
        nextTerm = t1 + t2;
        t1 = t2;
        t2 = nextTerm;
        
        cout << nextTerm << ", ";
    }
    return 0;
}"""

codes = {
    "factorial": cpp_code1,
    "fibonacci": cpp_code2
}

print("Компиляция в LLVM IR...")
# function_ir_fib = get_ir(codes['fibonacci'])
# function_ir_fact = get_ir(codes['factorial'])

with open("ir_test_files/fact.ll", "r") as file:
    function_ir_fact = file.read()

with open("ir_test_files/fib.ll", "r") as file:
    function_ir_fib = file.read()

print("Вызов c++ функции...")
module = llvm_python.parse_module(function_ir_fib) # Отправляется запрос на godbolt, где код компилируется clang11 в llvm-ir
print(module)
print(module.name)
# print("test")
# module.test()
# print("end test")
# module.printSummary()
# print(module)
# print(dir(module))
# print(module.__sizeof__())
# print(module.getName())
# print(module.getFunctions())
function = module.get_function("_Z9factoriali")
print(module.get_functions())
function_not_exists = module.get_function("main2")
print(function_not_exists)
# print(function)
# print(function.getName())
print("iteration")
for i in module.functions:
    print(i.name, "works!")

print(function)

blocks = list(function.blocks)
print(len(blocks))

for block in function.blocks:
    print(block)

print("arguments:")

for arg in function.args:
    print(arg)


blocks = list(function.blocks)
last_block = blocks[-2]
print("Instructions:")
instructions = last_block.getInstructions()
for instr in instructions:
    print(instr)

instruction = instructions[-2]

print("Instruction:")
print(instruction)
print("Operands:")
print(instruction.getOperand(0))
print(instruction.getOperand(1))
print("Return value:")
print(instruction.getValue())

print("Конец")
