import functools

def solve(a):
    if not a:
        return []

    # Try Timsort first
    try:
        return sorted(a)
    except NotImplementedError:
        # Fallback to Quicksort
        return functools.cmp_to_key(lambda x, y: 0 if x == y else (-1 if x < y else 1))(a)

    # If Timsort is not available, use Merge sort
    # Note: This is a simplified implementation and may not be fully correct
    if len(a) <= 1:
        return a

    # Merge sort
    left = a[:len(a)//2]
    right = a[len(a)//2:]
    return merge(sort(left), sort(right))

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result