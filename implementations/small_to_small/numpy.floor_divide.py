import operator

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x // y

    if isinstance(x, list) and isinstance(y, list):
        # Broadcast to common shape
        x = x + [0] * (len(y) - len(x)) if len(x) < len(y) else [0] * (len(x) - len(y)) + x
        y = y + [0] * (len(x) - len(y)) if len(y) < len(x) else [0] * (len(y) - len(x)) + y
        return [operator.truediv(a, b) for a, b in zip(x, y)]

    if isinstance(x, int) and isinstance(y, list):
        return [x // a for a in y]

    if isinstance(x, list) and isinstance(y, int):
        return [x // y]

    if not x or not y:
        return []