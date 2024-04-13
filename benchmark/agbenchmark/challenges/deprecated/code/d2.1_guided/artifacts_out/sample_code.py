from typing import List, Optional

def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Given an array of integers `nums` and an integer `target`, return
    indices of the two numbers such that they add up to `target`.

    If there are no two numbers that add up to `target`, return `None`.

    Parameters:
    nums (List[int]): list of integers
    target (int): target integer

    Returns:
    Optional[List[int]]: list of two indices that add up to target, or None
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None
