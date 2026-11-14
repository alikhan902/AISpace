def solve(a, n=1):
    if n == 0:
        return a[:]
    if n >= len(a):
        return []
    if len(a) == 1:
        return []
    first_diff = [a[i+1] - a[i] for i in range(len(a)-1)]
    return solve(first_diff, n-1)