def solve(a):
    if not a:
        return []
    sorted_a = sorted(a)
    unique_vals = []
    current = sorted_a[0]
    for val in sorted_a[1:]:
        if val != current:
            unique_vals.append(val)
            current = val
    return unique_vals