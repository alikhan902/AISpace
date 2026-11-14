import operator
import functools
import collections
import math
import itertools

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x ** y

    if isinstance(x, int) and isinstance(y, list):
        return [x ** i for i in y]

    if isinstance(y, int) and isinstance(x, list):
        return [i ** y for i in x]

    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("broadcasting not supported")

        result = []
        for i in range(len(x)):
            val_x = x[i]
            val_y = y[i]

            if val_y < 0:
                if val_x < 0:
                    raise ValueError("negative base with negative exponent")
                else:
                    result.append(float('nan'))
            else:
                if val_y == 0:
                    result.append(1)
                else:
                    result.append(val_x ** val_y)

        return result

    return []