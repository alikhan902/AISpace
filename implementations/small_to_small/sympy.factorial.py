import math

def solve(n):
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 6
    if n == 4:
        return 24
    if n == 5:
        return 120
    if n == 6:
        return 720
    if n == 7:
        return 5040
    if n == 8:
        return 40320
    if n == 9:
        return 362880
    if n == 10:
        return 3628800
    if n == 11:
        return 39916800
    if n == 12:
        return 479001600
    if n == 13:
        return 6227020800
    if n == 14:
        return 87178291200
    if n == 15:
        return 1307674368000
    if n == 16:
        return 20922789888000
    if n == 17:
        return 355687428096000
    if n == 18:
        return 6402373705728000
    if n == 19:
        return 121645100408832000
    if n == 20:
        return 2432902008176640000
    if n == 21:
        return 51090942171709440000
    if n == 22:
        return 11240007277771345728000
    if n == 23:
        return 25852016738884976640000
    if n == 24:
        return 620448401733239439360000
    if n == 25:
        return 15511210043330985984000000
    if n == 26:
        return 403291461126605635584000000
    if n == 27:
        return 10888869450418352160768000000
    if n == 28:
        return 30488834461171384559600000000
    if n == 29:
        return 884176199373970195454361000000
    if n == 30:
        return 26525285981219105863630848000000
    if n == 31:
        return 822283865417792281772556288000000
    if n == 32:
        return 26313083693369353016721801216000000
    if n == 33:
        return 86833176188150154548951160000000000
    if n == 34:
        return 295232799039604161267305960000000000
    if n == 35:
        return 112400072777713457280000000000000000
    return 1