import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        stacks_input, moves_input = parse_input("test_input", sep="\n\n")
        self.assertEqual(solve_part_1(stacks_input, moves_input), "CMZ")

    def test_part_2(self):
        stacks_input, moves_input = parse_input("test_input", sep="\n\n")
        self.assertEqual(solve_part_2(stacks_input, moves_input), "MCD")


if __name__ == "__main__":
    unittest.main()
