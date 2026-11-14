def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x // y
    elif isinstance(x, list) and isinstance(y, int):
        return [xi // y for xi in x]
    elif isinstance(x, int) and isinstance(y, list):
        return [x // yi for yi in y]
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("Lists must be of the same length for element-wise division")
        return [xi // yi for xi, yi in zip(x, y)]
    else:
        raise ValueError("Unsupported input types")