from typing import List, Union

def solve(x: Union[int, List[int]], y: Union[int, List[int]]) -> Union[int, List[int]]:
    if isinstance(x, int) and isinstance(y, int):
        return x % y
    
    # Handle scalar and list cases
    if isinstance(x, int):
        x = [x] * len(y)
    elif isinstance(y, int):
        y = [y] * len(x)

    # Check if both are lists
    if not isinstance(x, list) or not isinstance(y, list):
        raise ValueError("Both x and y must be lists after broadcasting")

    # Ensure lists are of the same length
    if len(x) != len(y):
        raise ValueError("Lists must be of the same length after broadcasting")

    # Compute remainders
    return [x_i % y_i for x_i, y_i in zip(x, y)]