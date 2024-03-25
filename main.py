import llvm_python  # Наша C++ библиотека

from compile_online import get_ir

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

cpp_code3 = """
int do_operation(int a, float& b, float& c)
{
    return a + b * c;
}

int main()
{
    float b = 5.0;
    float d = 5.0;
    int i = do_operation(5, b, d);
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

asm = """
define i32 @foo(i32 %a, i32 %b) {
  %c = add i32 1, 2
  %d = add i32 3, 4
  %e = add i32 %a, %b
  %f = add i32 %c, %d
  %g = add i32 %e, %f
  %k = add i32 8, 6
  ret i32 %g
}
"""

ir = get_ir(cpp_code3)
with open("./ir_test_files/test.ll", "w") as file:
    file.write(ir)

q = llvm_python.test(asm)

print(q)
print(q.__dict__)

print(dir(llvm_python))
mod = llvm_python.createModule(ir)
print("OK")
print(mod)
print(mod.functions)
print(mod.dict())


def visit_type(type, t):
    print("    " * t, "Type:")
    print("    " * t + type.name)
    print("    " * t + str(type.type_id))


def visit_block(block):
    pass


def visit_arg(arg, t):
    print("    " * t, "Arg:")
    print("    " * t + str(arg.position))
    print("    " * t + arg.name)
    print("    " * t + str(arg.parent))
    visit_type(arg.type, t)


def visit_function(function, t):
    print("    " * t, "Function:")
    print("    " * t + function.name)
    visit_type(function.type, t)
    for arg in function.args:
        visit_arg(arg, t + 1)

    for attribute_set in function.attributes:
        for attribute in attribute_set:
            print(attribute)

    # for block in function.blocks:
    #     visit_block(block)


def visit_module(module, t=1):
    print("Module:")
    print("    " + mod.name)
    for function in mod.functions:
        visit_function(function, t + 1)

f = None

# visit_module(mod)
for function in mod.functions:
    if "main" in function.name:
        f = function
        break

print(f)
