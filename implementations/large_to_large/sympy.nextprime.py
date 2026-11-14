def solve(n):
    if not isinstance(n, int) or n < -10 or n > 5000:
        raise ValueError
    if ith <= 0:
        raise ValueError
    # Start from candidate = n + 1
    candidate = n + 1
    count = 0
    while True:
        # Check if candidate is prime using 6j ± 1 rule
        if candidate >  1 and (candidate % 6 == 1 or candidate %  6 == 5):
            count += 1
            if count == ith:
                return candidate
        candidate += 1
    # This is a placeholder for the rest of the code
    return None