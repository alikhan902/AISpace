import functools

def solve(a):
    if not a:
        return []

    # Handle single dimension
    if len(a) == 1:
        return [a[0]]

    # Sort along the last axis (default)
    if len(a) > 1:
        # Flatten if needed
        if a[-1] is None:
            a = [item for item in a]
        else:
            a = [item for item in a]
        # Sort using timsort for integers
        a = sorted(a, key=functools.cmp_to_key(lambda x, y: (x < y) - (y < x)))
        return a

    return a