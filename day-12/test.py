import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_line, solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        heights_array = parse_input("test_input", parse_fn=parse_line)
        self.assertEqual(solve_part_1(heights_array), 31)

    def test_part_2(self):
        heights_array = parse_input("test_input", parse_fn=parse_line)
        self.assertEqual(solve_part_2(heights_array), 29)


if __name__ == "__main__":
    unittest.main()
