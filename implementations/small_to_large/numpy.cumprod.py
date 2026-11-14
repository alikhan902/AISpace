def solve(a):
    if not a:
        return []
    result = [a[0]]
    for num in a[1:]:
        result.append(result[-1] * num)
    return result