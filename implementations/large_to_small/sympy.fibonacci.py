from collections import defaultdict

def solve(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Fibonacci numbers
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    # Fibonacci polynomials
    if n == 1:
        return 1
    elif n == 2:
        return lambda x: x
    else:
        coeffs = [0] * (n + 1)
        coeffs[1] = 1
        coeffs[2] = x
        for i in range(3, n + 1):
            coeffs[i] = x * coeffs[i - 1] + coeffs[i - 2]
        return coeffs
