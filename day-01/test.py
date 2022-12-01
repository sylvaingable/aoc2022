import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import parse_input
from solution import (
    parse_snacks,
    greatest_total_calories,
    top_three_total_calories,
)


class TestDay1(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = parse_input(path="test_input", sep="\n\n", parse_fn=parse_snacks)

    def test_part_1(self):
        self.assertEqual(greatest_total_calories(self.data), 24000)

    def test_part_2(self):
        self.assertEqual(top_three_total_calories(self.data), 45000)


if __name__ == "__main__":
    unittest.main()
