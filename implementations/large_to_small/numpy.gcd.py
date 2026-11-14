import math

def solve(x, y):
    if not (isinstance(x, (int, list)) and isinstance(y, (int, list))):
        raise ValueError("Inputs must be integers or 1-D lists of integers.")

    if isinstance(x, int) and isinstance(y, int):
        return math.gcd(abs(x), abs(y))

    if isinstance(x, int):
        x = [x]
    if isinstance(y, int):
        y = [y]

    if len(x) != len(y):
        # Broadcast to the length of the longer list
        x = x + [0] * (len(y) - len(x)) if len(x) < len(y) else y + [0] * (len(x) - len(y))
    else:
        x = x[:]
        y = y[:]

    result = []
    for a, b in zip(x, y):
        result.append(math.gcd(abs(a), abs(b)))

    return result