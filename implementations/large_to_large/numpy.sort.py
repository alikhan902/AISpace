def solve(a):
    if not isinstance(a, list):
        raise ValueError("Input must be a list")
    
    # Handle empty list
    if len(a) == 0:
        return []

    # Check for NaN values
    has_nan = False
    for x in a:
        if isinstance(x, float) and math.isnan(x):
            has_nan = True
            break

    # If there are NaNs, we need to handle them by placing at the end
    if has_nan:
        # Create a list of non-NaN values and NaNs
        non_nan = [x for x in a if not math.isnan(x)]
        nan_count = len(a) - len(non_nan)
        # Sort non-NaN values
        non_nan_sorted = sorted(non_nan)
        # Return sorted non-N.ans + [float('nan')] * nan_count
        return non_nan_sorted + [float('nan')] * nan_count

    # Check for complex numbers
    has_complex = any(isinstance(x, complex) for x in a)
    if has_complex:
        # Sort complex numbers lexicographically
        # Real part first, then imaginary part
        sorted_complex = sorted(a, key=lambda x: (x.real, x.imag))
        return sorted_complex

    # Check for multi-dimensional arrays
    # Since the input is specified as a one-dimensional list, we assume it's 1D
    # But the card says: 'For multi-dimensional arrays, sort along the specified axis (default: last axis) by flattening the array if axis is None.'
    # However, the input is defined as a one-dimensional list, so we don't need to handle multi-dimensional here.
    # But the card says: 'The input is a one-dimensional list of integers, possibly empty'
    # So we assume 1D

    # Sort the list using a stable sort (timsort for integers)
    # Since the input is integers, we can use sorted() which is stable for integers
    return sorted(a)
