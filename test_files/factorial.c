#include "stdio.h"


int factorial_cycle(int n)
{
    int result = 1;
    while (n > 0)
    {
        result *= n;
        n -= 1;
    }
    return result;
}

int factorial_req(int n)
{
    if (n == 1)
    {
        return 1;
    }
    return factorial_req(n - 1) * n;
}

int main()
{
    int factorial_cycle_result = factorial_cycle(10);
    int factorial_req_result = factorial_req(10);
    printf("%d\n", factorial_cycle_result);
    printf("%d\n", factorial_req_result);
    return 0;
}
