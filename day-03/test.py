import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import split_rucksack_content, solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        rucksacks_contents = parse_input("test_input", parse_fn=split_rucksack_content)
        self.assertEqual(solve_part_1(rucksacks_contents), 157)

    def test_part_2(self):
        all_rucksacks = parse_input("test_input", parse_fn=tuple)
        self.assertEqual(solve_part_2(all_rucksacks), 70)


if __name__ == "__main__":
    unittest.main()
