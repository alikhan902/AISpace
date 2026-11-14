def solve(a, minlength=0):
    if not a:
        return [0] if minlength <= 1 else [0]

    max_val = max(a)
    output = [0] * (max_val + 2)

    for num in a:
        output[num] += 1

    if minlength > 0:
        output = output[:minlength]

    return output