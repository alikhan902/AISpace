def solve(a):
    count = 0
    for element in a:
        if isinstance(element, int):
            if element != 0:
                count += 1
        elif isinstance(element, list):
            count += solve(element)
    return count