def solve(n):
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < -10 or n > 5000:
        raise ValueError("n must be within the range -10 to 5000")
    
    # Handle edge case: ith = 0
    if ith == 0:
        raise ValueError("ith must be greater than 0")
    
    # Generate primes greater than n
    def is_prime(x):
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        # Check using 6*j ± 1
        i = 3
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0:
                return False
            i += 6
        return True

    # Start from n + 1 and find the ith prime
    count = 0
    num = n + 1
    while True:
        if is_prime(num):
            count += 1
            if count == ith:
                return num
        num += 1

    # This line should never be reached
    return None