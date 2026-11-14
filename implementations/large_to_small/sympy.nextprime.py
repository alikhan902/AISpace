import math

def solve(n):
    if not isinstance(n, int) or n < -10 or n > 5000:
        raise ValueError("n must be an integer between -10 and 5000")

    if n <= 0:
        i = 1
    else:
        i = 1
        while True:
            i += 1
            candidate = n + i
            if candidate < 2:
                continue
            if candidate % 6 == 1 or candidate % 6 == 5:
                if candidate > 1:
                    break
            else:
                continue
    return i