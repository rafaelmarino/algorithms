# Uses python3


def fibo(n):
    # Fib Series = 0,1,1,2,3,5,8,13
    a = 0  # Not the first element, but rather the 2nd
    b = 1  # The 3rd element
    result = 0

    if n == 0:
        return result
    else:
        result = 1
        for i in range(1, n):
            result = a + b
            a = b
            b = result
        return result


n = int(input())
print(fibo(n))
