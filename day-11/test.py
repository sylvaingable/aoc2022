import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_monkey, solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        monkeys = parse_input("test_input", sep="\n\n", parse_fn=parse_monkey)
        self.assertEqual(solve_part_1(monkeys), 10605)

    def test_part_2(self):
        monkeys = parse_input("test_input", sep="\n\n", parse_fn=parse_monkey)
        self.assertEqual(solve_part_2(monkeys), 2713310158)


if __name__ == "__main__":
    unittest.main()
