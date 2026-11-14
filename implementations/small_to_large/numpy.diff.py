def solve(a, n=1):
    if n == 0:
        return a[:]
    if n > len(a):
        return []
    result = [a[0]]
    for i in range(1, len(a)):
        diff = a[i] - a[i-1]
        result.append(diff)
    return result