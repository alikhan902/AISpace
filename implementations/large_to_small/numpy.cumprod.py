import numpy as np

def solve(a):
    if not a:
        return []
    
    # Ensure input is a 1D list
    if len(a) == 1:
        return int(a[0])
    
    # Compute cumulative product along specified axis
    axis = 0 if len(a[0]) == 1 else 1
    result = np.cumprod(a, axis=axis)
    
    # Handle output format
    if len(result) == 1:
        return int(result[0])
    else:
        return result.tolist()