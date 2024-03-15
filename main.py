import llvm_python # Наша C++ библиотека
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

codes = {
    "fibonacci": cpp_code1,
    "factorial": cpp_code2
}

print("Компиляция в LLVM IR...")
function_ir = get_ir(codes['factorial'])

print("Вызов c++ функции...")
function_names = llvm_python.parseModuleFunctions(function_ir) # Отправляется запрос на godbolt, где код компилируется clang11 в llvm-ir

print("Ура, список функций получен!")
print(function_names)
