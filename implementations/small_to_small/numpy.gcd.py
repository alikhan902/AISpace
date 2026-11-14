import math

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return math.gcd(x, y)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("Input lists must be of the same length")
        return [math.gcd(abs(x[i]), abs(y[i])) for i in range(len(x))]
    elif isinstance(x, int):
        return [math.gcd(abs(x), y)]
    elif isinstance(y, int):
        return [math.gcd(abs(x), y)]
    else:
        raise ValueError("Unsupported input types")