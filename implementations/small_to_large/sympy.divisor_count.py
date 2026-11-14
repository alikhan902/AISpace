def solve(n):
    if n == 1:
        return 1
    count = 0
    for i in range(1, int(n ** 0.5) + 
    if n % i == 0:
        count += 1
    return count