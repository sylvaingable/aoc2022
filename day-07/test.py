import os
import unittest
import sys


sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_terminal_command, solve_part_1, solve_part_2
from utils import parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        terminal_session = parse_input(
            "test_input", sep="\n$ ", parse_fn=parse_terminal_command
        )[1:]
        self.assertEqual(solve_part_1(terminal_session), 95437)

    def test_part_2(self):
        terminal_session = parse_input(
            "test_input", sep="\n$ ", parse_fn=parse_terminal_command
        )[1:]
        self.assertEqual(solve_part_2(terminal_session), 24933642)


if __name__ == "__main__":
    unittest.main()
