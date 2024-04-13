from sample_code import multiply_int

def test_multiply_int(num: int, multiplier, expected_result: int) -> None:
    result = multiply_int(num, multiplier)
    assert result == expected_result, (
        f"AssertionError: Expected the output to be {expected_result} "
        f"but got {result}"
    )

if __name__ == "__main__":
    # test the trivial case
    num = 4
    multiplier = 2
    expected_result = 8
    test_multiply_int(num, multiplier, expected_result)

    # test another case
    num = 5
    multiplier = 3
    expected_result = 15
    test_multiply_int(num, multiplier, expected_result)

    # test negative numbers
    num = -3
    multiplier = -4
    expected_result = 12
    test_multiply_int(num, multiplier, expected_result)
