import bisect

def solve(a, v, side='left'):
    if not a:
        return 0 if side == 'left' else len(a)

    if isinstance(v, list):
        return [bisect.bisect_left(a, x, lo=0, hi=len(a), side_effect=False) for x in v]

    # For scalar v, use bisect_left
    return bisect.bisect_left(a, v, lo=0, hi=len(a), side_effect=False)