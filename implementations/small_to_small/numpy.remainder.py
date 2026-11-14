import numpy as np

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x % y

    if isinstance(x, int):
        x = [x]
    if isinstance(y, int):
        y = [y]

    if len(x) != len(y):
        x = np.broadcast(x, y)
        y = np.broadcast(x, y)

    result = [x[i] % y[i] for i in range(len(x))]
    return result