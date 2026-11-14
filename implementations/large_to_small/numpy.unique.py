import collections

def solve(a):
    if not a:
        return []

    # Sort the input list
    sorted_a = sorted(a)

    # Initialize variables
    unique = []
    prev = sorted_a[0]
    count = 1

    # Track first occurrence indices
    first_occurrence = []
    # Track inverse indices for reconstruction
    inverse_indices = []
    # Track counts of each unique value
    counts = []

    # Iterate through the sorted list
    for i, val in enumerate(sorted_a):
        if val != prev:
            unique.append(val)
            first_occurrence.append(i)
            inverse_indices.append(i)
            counts.append(count)
            prev = val
            count = 1
        else:
            count += 1

    # If all elements are the same, return a single value
    if len(unique) == 1:
        return unique

    # Return the sorted unique values
    return unique