def solve(a):
    if isinstance(a, int):
        return 1 if a != 0 else 0
    elif isinstance(a, list):
        count = 0
        for item in a:
            count += solve(item)
        return count
    else:
        return 0