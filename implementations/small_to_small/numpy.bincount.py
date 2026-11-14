from collections import defaultdict

def solve(a, minlength=0):
    if not a:
        return []

    if not isinstance(a, list) or not all(isinstance(x, int) for x in a):
        raise ValueError('Input must be a list of nonnegative integers')

    max_val = max(a)

    if minlength < 0:
        raise ValueError('minlength must be a nonnegative integer')

    if minlength > max_val:
        raise ValueError('minlength must be less than or equal to the maximum value in the input list')

    counts = defaultdict(int)
    for num in a:
        counts[num] += 1

    output = [0] * (max_val + 1)
    for num, count in counts.items():
        output[num] = count

    return output