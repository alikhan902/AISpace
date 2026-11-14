from math import sqrt

def solve(n):
    if n == 1:
        return 1

    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            if (i - 1) * (n // i) % i == 0:
                result = result * (i - 1) // i * (n // i - 1) // i
                result += (i - 1)
            else:
                result = result * (i - 1) // i * (n // i - 1) // i
                result += (i - 1)
        i += 1
    return result