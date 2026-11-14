def solve(a):
    if not a:
        return []
    
    # Sort the array
    sorted_a = sorted(a)
    
    # Remove duplicates while preserving order
    result = []
    for num in sorted_a:
        if not result or result[-1] != num:
            result.append(num)
    
    return result