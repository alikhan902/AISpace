def solve(n):
    if n == 1:
        return [1]
    divisors = []
    for i in range(1, int(n ** 0.5) + 
    if i * i == n:
        divisors.append(i)
    elif n % i == 0:
        divisors.append(i)
        divisors.append(n // i)
    divisors.sort()
    return divisors