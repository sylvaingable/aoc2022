import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        data_stream, *_ = parse_input("test_input")
        self.assertEqual(solve_part_1(data_stream), 10)

    def test_part_2(self):
        data_stream, *_ = parse_input("test_input")
        self.assertEqual(solve_part_2(data_stream), 29)


if __name__ == "__main__":
    unittest.main()
