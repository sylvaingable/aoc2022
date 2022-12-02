import os
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import parse_input
from solution import (
    parse_input,
    parse_turn_choices,
    parse_turn_strategy,
    turn_choices_from_strategy,
    total_score_from_turns_choices,
)


class TestDay1(unittest.TestCase):
    def test_part_1(self):
        turns_choices = parse_input(
            path="test_input", sep="\n", parse_fn=parse_turn_choices
        )
        self.assertEqual(total_score_from_turns_choices(turns_choices), 15)

    def test_part_2(self):
        turns_strategies = parse_input(
            path="test_input", sep="\n", parse_fn=parse_turn_strategy
        )
        turns_choices = (turn_choices_from_strategy(s) for s in turns_strategies)
        self.assertEqual(total_score_from_turns_choices(turns_choices), 12)


if __name__ == "__main__":
    unittest.main()
