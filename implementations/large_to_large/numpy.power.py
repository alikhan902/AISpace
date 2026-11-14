def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return int(x ** y)
    elif isinstance(x, int) and isinstance(y, list):
        return [int(x ** y_i) for y_i in y]
    elif isinstance(x, list) and isinstance(y, int):
        return [int(x_i ** y) for x_i in x]
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("Lists must be same length")
        return [int(x_i ** y_i) for x_i, y_i in zip(x, y)]
    else:
        raise ValueError("Inputs must be integers or 1-D lists of integers")