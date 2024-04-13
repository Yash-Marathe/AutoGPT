# mypy: ignore-errors
from typing import List, NamedTuple, Any

from sample_code import three_sum

class TestCase(NamedTuple):
    nums: List[int]

