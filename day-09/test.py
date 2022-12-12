import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import flatten, parse_input
from solution import motions_vectors_from_line, parse_input, solve_part_1, solve_part_2


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        motions_vectors = flatten(
            parse_input("test_input", parse_fn=motions_vectors_from_line)
        )
        self.assertEqual(solve_part_1(motions_vectors), 13)

    def test_part_2(self):
        motions_vectors = flatten(
            parse_input("test_input", parse_fn=motions_vectors_from_line)
        )
        self.assertEqual(solve_part_2(motions_vectors), 1)
        motions_vectors = flatten(
            parse_input("test_input_2", parse_fn=motions_vectors_from_line)
        )
        self.assertEqual(solve_part_2(motions_vectors), 36)


if __name__ == "__main__":
    unittest.main()
