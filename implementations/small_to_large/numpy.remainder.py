def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x % y
    elif isinstance(x, int) and isinstance(y, list):
        return [x % y_i for y_i in y]
    elif isinstance(x, list) and isinstance(y, int):
        return [x_i % y for x_i in x]
    else:
        return [x_i % y_i for x_i, y_i in zip(x, y)]