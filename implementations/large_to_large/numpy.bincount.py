def solve(a, minlength=0):
    if not a:
        return [0]
    max_val = max(a)
    output = [0] * (max_val + 1)
    for num in a:
        if num <= max_val:
            output[num] += 1
    if minlength > 0:
        output += [0] * (minlength - len(output))
    return output