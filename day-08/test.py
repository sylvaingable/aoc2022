import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_line, solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        from rich import print

        grid = parse_input("test_input", parse_fn=parse_line)
        self.assertEqual(solve_part_1(grid), 21)

    def test_part_2(self):
        grid = parse_input("test_input", parse_fn=parse_line)
        self.assertEqual(solve_part_2(grid), 8)


if __name__ == "__main__":
    unittest.main()
