def solve(a, minlength=0):
    if not all(x >= 0 for x in a):
        raise ValueError("Input list contains negative values")
    max_val = max(a) if a else 0
    if minlength < 0:
        raise ValueError("minlength is negative")
    if minlength > max_val:
        raise ValueError("minlength is greater than max value")
    output = [0] * (max_val +  1)
    for num in a:
        if num <= max_val:
            output[num] += 1
    if minlength > 0:
        output = output[:minlength]
    return output