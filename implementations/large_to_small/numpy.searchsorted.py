import bisect

def solve(a, v, side='left'):
    if not a:
        return 0

    if isinstance(v, list):
        return [bisect.bisect_left(a, x, lo=0, hi=len(a)) for x in v]

    # Handle scalar value
    if side == 'left':
        return bisect.bisect_left(a, v)
    elif side == 'right':
        return bisect.bisect_right(a, v)
    else:
        raise ValueError("Invalid side value. Must be 'left' or 'right'.")