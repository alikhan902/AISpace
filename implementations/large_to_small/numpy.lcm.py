import math
import functools
import operator
import collections
import fractions
import operator

def solve(x, y):
    if isinstance(x, list) and isinstance(y, list):
        # Broadcast if shapes differ
        shape_x = len(x)
        shape_y = len(y)
        if shape_x != shape_y:
            # Broadcast using standard rules
            broadcasted_x = x if shape_x == 1 else [x[i] for i in range(shape_x)]
            broadcasted_y = y if shape_y == 1 else [y[i] for i in range(shape_y)]
            # Compute LCM for each pair
            result = []
            for i in range(max(shape_x, shape_y)):
                a = broadcasted_x[i] if i < len(broadcasted_x) else 0
                b = broadcasted_y[i] if i < len(broadcasted_y) else 0
                if a == 0 and b == 0:
                    result.append(0)
                else:
                    g = fractions.gcd(a, b)
                    lcm = (a * b) // g
                    result.append(lcm)
            return result
        else:
            # Same shape, return list of LCMs
            return [fractions.lcm(x[i], y[i]) for i in range(len(x))]
    elif isinstance(x, int) and isinstance(y, int):
        return fractions.lcm(x, y)
    else:
        # One is a list, the other is a scalar
        if isinstance(x, int):
            return [fractions.lcm(x, y)]
        else:
            return [fractions.lcm(x[i], y) for i in range(len(x))]
