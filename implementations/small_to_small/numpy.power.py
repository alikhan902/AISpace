import operator
import math
import functools
import collections
import heapq
import fractions
import operator

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        if x == 0 and y == 0:
            return 1
        return x ** y

    if isinstance(x, int) and not isinstance(y, int):
        return [y[i] ** x for i in range(len(y))]

    if not isinstance(x, int) and isinstance(y, int):
        return [x[i] ** y for i in range(len(x))]

    if len(x) != len(y):
        raise ValueError("x and y must be broadcastable to the same shape.")

    result = []
    for i in range(len(x)):
        x_val = x[i]
        y_val = y[i]

        if y_val < 0:
            if not isinstance(y_val, int):
                raise ValueError("Negative values raised to non-integer exponents result in nan.")
            if y_val > 8:
                raise ValueError("Exponents must be integers in 0..8.")
            if y_val == 0:
                if x_val == 0:
                    result.append(1)
                else:
                    result.append(x_val ** y_val)
            else:
                result.append(x_val ** y_val)
        else:
            if y_val == 0:
                if x_val == 0:
                    result.append(1)
                else:
                    result.append(1)
            else:
                result.append(x_val ** y_val)

    return result