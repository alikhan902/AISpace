def solve(n):
    if n < 0 or n > 35:
        raise ValueError("n must be in 0 to 35 inclusive")
    
    # Compute binomial coefficient binomial(2n, n)
    def binom(a, b):
        if b < 0 or b > a:
            return 0
        if b > a - b:
            b = a - b
        num = 1
        for i in range(1, b + 1):
            num = num * (a - i + 1) // i
        return num

    binom_2n_n = binom(2 * n, n)
    catalan = binom_2n_n // (n +  1)
    return catalan