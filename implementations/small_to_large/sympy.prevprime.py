def solve(n):
    if n <= 2:
        return 2
    # Generate candidates: 6*j - 1 and 6*j + 1
    # We need to find the largest prime < n
    # Start from j = (n-1)//6 down to 0
    j = (n - 1) // 6
    while j >= 0:
        candidate1 = 6 * j - 1
        candidate2 = 6 * j + 1
        # Check if candidate1 is prime
        if candidate1 >= 2 and candidate1 < n:
            if is_prime(candidate1):
                return candidate1
        # Check if candidate2 is prime
        if candidate2 >= 2 and candidate2 < n:
            if is_prime(candidate2):
                return candidate2
        j -= 1
    return 2

def is_prime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    # Check odd factors up to sqrt(x)
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True