import operator

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x // y

    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("Inputs must be of the same length or broadcastable to the same length.")

        result = []
        for a, b in zip(x, y):
            if b == 0:
                raise ValueError("Denominator must be nonzero.")
            result.append(a // b)
        return result

    if isinstance(x, int):
        return x // y

    if isinstance(y, int):
        return x // y

    raise ValueError("Unsupported input types.")