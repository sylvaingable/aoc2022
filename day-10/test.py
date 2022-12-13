import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from solution import parse_instruction, solve_part_1, solve_part_2
from utils import flatten, parse_input


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        instructions = tuple(
            flatten(parse_input("test_input", parse_fn=parse_instruction))
        )
        self.assertEqual(solve_part_1(instructions), 13140)

    def test_part_2(self):
        instructions = tuple(
            flatten(parse_input("test_input", parse_fn=parse_instruction))
        )
        self.assertListEqual(
            solve_part_2(instructions),
            [
                "##..##..##..##..##..##..##..##..##..##..",
                "###...###...###...###...###...###...###.",
                "####....####....####....####....####....",
                "#####.....#####.....#####.....#####.....",
                "######......######......######......####",
                "#######.......#######.......#######.....",
            ],
        )


if __name__ == "__main__":
    unittest.main()
