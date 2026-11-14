def solve(a):
    if not a:
        return []
    
    # Handle the case where the input is a single element
    if len(a) == 1:
        return a[0]
    
    # Compute cumulative product
    product = 1
    result = []
    for num in a:
        product *= num
        result.append(product)
        
    return result