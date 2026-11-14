import functools

def solve(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    def fib_polynomial(n, x):
        if n == 0:
            return 1
        if n == 1:
            return x
        return x * fib_polynomial(n - 1, x) + fib_polynomial(n - 2, x)

    return fib_polynomial(n, 1)

if __name__ == '__main__':
    print(solve(100))