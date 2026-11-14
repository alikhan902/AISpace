import functools

def solve(a):
    if not a:
        return []

    result = [a[0]]
    for i in range(1, len(a)):
        result.append(result[-1] * a[i])

    return result