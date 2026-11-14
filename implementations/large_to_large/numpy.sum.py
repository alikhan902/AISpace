def solve(a):
    if not a:
        return 0
    total = 0
    for num in a:
        total = total + num
        if total > 2**63 - 1 or total < -2**63:
            total = total % (2**64)
    return total