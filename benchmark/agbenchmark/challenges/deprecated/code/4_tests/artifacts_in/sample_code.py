def multiply_num(num: float = 1.0) -> float:
    """
    Multiplies a given number by 2.

    Args:
    num (float): The number to be multiplied. Defaults to 1.0.

    Returns:
    float: The multiplied number.

    Raises:
    TypeError: If the input is not a number.
    ValueError: If the input is negative.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Input must be a number.")
    if num < 0:
        raise ValueError("Input cannot be negative.")

    multiplied_num = num * 2
    return multiplied_num
