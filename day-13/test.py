import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_packets_pair, solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        packets_pairs = parse_input(
            "test_input", sep="\n\n", parse_fn=parse_packets_pair
        )
        self.assertEqual(solve_part_1(packets_pairs), 13)

    def test_part_2(self):
        packets_pairs = parse_input(
            "test_input", sep="\n\n", parse_fn=parse_packets_pair
        )
        self.assertEqual(solve_part_2(packets_pairs), 140)


if __name__ == "__main__":
    unittest.main()
