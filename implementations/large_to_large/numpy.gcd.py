import math

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return math.gcd(abs(x), abs(y))
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("Lists must be of the same length for list/list inputs")
        return [math.gcd(abs(a), abs(b)) for a, b in zip(x, y)]
    elif isinstance(x, int) and isinstance(y,  list):
        return [math.gcd(abs(x), abs(b)) for b in y]
    elif isinstance(x, list) and isinstance(y, int):
        return [math.gcd(abs(a), abs(y)) for a in x]
    else:
        raise ValueError("Inputs must be integers or 1-D lists of integers")