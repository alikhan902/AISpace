import functools

def solve(a):
    if not a:
        return 0

    if len(a) == 1:
        return a[0]

    if axis is None:
        return sum(a)

    # Handle axis specification
    if axis == 0:
        return functools.reduce(lambda x, y: x + y, a)
    elif axis == 1:
        return [functools.reduce(lambda x, y: x + y, sub) for sub in zip(*a)]
    else:
        raise ValueError("Invalid axis value")

    # Handle integer overflow
    max_int = 2**63 - 1
    if sum(a) > max_int:
        return sum(a) % (2**64)
    else:
        return sum(a)