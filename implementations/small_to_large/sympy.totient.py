def solve(n):
    if n == 1:
        return 1
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            j = n // i
            if math.gcd(i, j) == 1:
                result = result * (i - 1) // i + (j - 1)
            else:
                result = result * (i - 1) // i
            n = n // i
        i += 1
    if n > 1:
        result = result * (n - 1) // n
    return result