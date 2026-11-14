def solve(a, n=1):
    if not a:
        return []

    if n == 0:
        return a.copy()

    if n >= len(a):
        return []

    # Compute the first difference
    diff = [a[i+1] - a[i] for i in range(len(a)-1)]

    # Apply the first difference n-1 times
    for _ in range(n-1):
        diff = [diff[i+1] - diff[i] for i in range(len(diff)-1)]

    return diff