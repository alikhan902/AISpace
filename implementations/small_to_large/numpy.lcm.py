import math
from typing import List, Union

def solve(x: Union[int, List[int]], y: Union[int, List[int]]) -> Union[int, List[int]]:
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def abs_list(lst):
        return [abs(num) for num in lst]

    def lcm(a, b):
        return a * b // gcd(a, b)

    if isinstance(x, int) and isinstance(y, int):
        return lcm(abs(x), abs(y))
    elif isinstance(x, int):
        y_abs = abs_list(y)
        return [lcm(abs(x), num) for num in y_abs]
    elif isinstance(y, int):
        x_abs = abs_list(x)
        return [l  # ... (truncated)
    else:
        x_abs = abs_list(x)
        y_abs = abs_list(y)
        if len(x_abs) != len(y_abs):
            raise ValueError("Inputs must be of the same length or broadcastable to a common shape. But they are not.")
        return [lcm(x_abs[i], y_abs[i]) for i in range(len(x_abs))]

# ... (truncated)