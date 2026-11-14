import math

def solve(x, y):
    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("Lists must be of the same length")
        return [math.floor(a / b) for a, b in zip(x, y)]
    elif isinstance(x, list):
        if isinstance(y, int):
            return [math.floor(a / y) for a in x]
        elif isinstance(y, list):
            if len(y) != 1:
                raise ValueError("List y must be of length  1 for scalar/list broadcasting")
            return [math.floor(a / y[0]) for a in x]
    elif isinstance(y, list):
        if isinstance(x, int):
            return [math.floor(x / b) for b in y]
    else:
        return math.floor(x / y)

    # Handle empty lists
    if isinstance(x, list) and isinstance(y, list) and len(x) == 0 and len(y) == 0:
        return []
    # This should not happen due to the above checks, but to be safe
    raise ValueError("Invalid input types")