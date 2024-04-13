from typing import List, Tuple

def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

    :param nums: List[int]
    :param target: int
    :return: Tuple[int, int]
    """
    pass


import unittest
from solution import two_sum

def test_two_sum(nums: List[int], target: int, expected_result: Tuple[int, int]) -> None:
    """
    Test the two_sum function.

    :param nums: List[int]
    :param target: int
    :param expected_result: Tuple[int, int]
    :return: None
    """
    result = two_sum(nums, target)
    print(result)
    assert result == expected_result, (
        f"AssertionError: Expected the output to be {expected_result}, "
        f"but got {result}"
    )


class TestTwoSum(unittest.TestCase):
    def test_trivial_case(self):
        nums = [2, 7, 11, 15]
        target = 9
        expected_result = (0, 1)
        self.assertEqual(test_two_sum(nums, target, expected_result),
