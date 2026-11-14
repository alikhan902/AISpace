import functools

def solve(a):
    if not a:
        return 1

    result = 1
    for num in a:
        result = result * num

    return result