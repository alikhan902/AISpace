import math
from typing import List

def solve(x: int, y: int) -> int:
    return math.lcm(abs(x), abs(y))

def solve(x: List[int], y: List[int]) -> List[int]:
    return [math.lcm(abs(a), abs(b)) for a, b in zip(x, y)]

def solve(x: int, y: List[int]) -> List[int]:
    return [math.lcm(abs(x), abs(y_i)) for y_i in y]

def solve(x: List[int], y: int) -> List[int]:
    return [math.l  # ... (truncated)