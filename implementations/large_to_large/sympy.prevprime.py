def solve(n):
    if n <= 2:
        raise ValueError("n must be at least 3")
    # Start from n-1 and decrement by 1 until a prime number is found
    candidate = n - 1
    # Use the 6j +/- 1 pattern to optimize the search
    while True:
        # Check if candidate is prime
        if candidate == 2:
            return 2
        if candidate % 2 ==  0 or candidate % 3 == 0:
            candidate -= 1
            continue
        # Check divisibility by integers up to the square root of the candidate
        i = 5
        while i * i <= candidate:
            if candidate % i == 0 or candidate % (i + 2) == 0:
                candidate -= 1
                break
            i += 6
        else:
            return candidate
    # This point should never be reached
    return None