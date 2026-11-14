import operator

def solve(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return x % y

    if isinstance(x, int) and isinstance(y, list):
        return [x % val for val in y]

    if isinstance(y, int) and isinstance(x, list):
        return [val % x for val in x]

    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            raise ValueError("broadcasting not supported")

        result = []
        for i in range(len(x)):
            if isinstance(x[i], int) and isinstance(y[i], int):
                result.append(x[i] % y[i])
            else:
                # Broadcast scalar to list
                if isinstance(x[i], int):
                    result.append(x[i] % y[i])
                elif isinstance(y[i], int):
                    result.append(x[i] % y[i])
                else:
                    result.append(x[i] % y[i])
        return result

    return []