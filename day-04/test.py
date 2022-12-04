import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_assignments_pair, solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        assignments_pairs = parse_input("test_input", parse_fn=parse_assignments_pair)
        self.assertEqual(solve_part_1(assignments_pairs), 2)

    def test_part_2(self):
        assignments_pairs = parse_input("test_input", parse_fn=parse_assignments_pair)
        self.assertEqual(solve_part_2(assignments_pairs), 4)


if __name__ == "__main__":
    unittest.main()
