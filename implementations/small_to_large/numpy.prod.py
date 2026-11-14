def solve(a):
    if len(a) == 0:
        return 1
    product = 1
    for x in a:
        product *= x
    return product