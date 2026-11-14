import math

def solve(x, y):
    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            x = [x[i] for i in range(max(len(x), len(y)))]
            y = [y[i] for i in range(max(len(x), len(y)))]
        return [solve(x[i], y[i]) for i in range(len(x))]

    if isinstance(x, int) and isinstance(y, int):
        return abs(x * y) // math.gcd(abs(x), abs(y))

    if isinstance(x, int):
        return [solve(x, y)]

    if isinstance(y, int):
        return [solve(x, y)]

    return ValueError('Inputs must be integers or 1-D lists of integers')