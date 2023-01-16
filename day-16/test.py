import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_line, solve_part_1, solve_part_2  # noqa: E402
from utils import parse_input  # noqa: E402


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        valves_graph = dict(parse_input("test_input", parse_fn=parse_line))
        self.assertEqual(solve_part_1(valves_graph), 1651)

    def test_part_2(self):
        pass


if __name__ == "__main__":
    unittest.main()
