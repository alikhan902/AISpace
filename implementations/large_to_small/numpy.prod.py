def solve(a):
    if not a:
        return 1

    result = 1
    for num in a:
        result = result * num
        if result > 2**63 - 1 or result < -2**63:
            # Handle overflow by using modular arithmetic
            # Since we cannot raise an error, we use modular arithmetic
            # This is a simplified approach and does not handle all cases
            # For full modular arithmetic, a more complex implementation is needed
            # Here we just handle the overflow by truncating
            result = result % 2**64

    return result