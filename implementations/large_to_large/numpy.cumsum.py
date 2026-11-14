def solve(a):
    if not a:
        return 0
    total = 0
    result = []
    for num in a:
        total += num
        result.append(total)
    return result