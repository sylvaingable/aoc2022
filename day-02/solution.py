from __future__ import annotations

import os
import sys
from enum import IntEnum
from typing import Iterable

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import parse_input


class TurnOutcome(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6

    @classmethod
    def parse(cls, char: str) -> TurnOutcome:
        return {"X": cls.LOSE, "Y": cls.DRAW, "Z": cls.WIN}[char]


class PlayerChoice(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def parse(cls, char: str) -> PlayerChoice:
        return {
            "A": cls.ROCK,
            "X": cls.ROCK,
            "B": cls.PAPER,
            "Y": cls.PAPER,
            "C": cls.SCISSORS,
            "Z": cls.SCISSORS,
        }[char]

    @classmethod
    def from_opponent_choice(
        cls, opponent_choice: PlayerChoice, outcome: TurnOutcome
    ) -> PlayerChoice:
        match outcome:
            case TurnOutcome.LOSE:
                return next(choice for choice in cls if choice < opponent_choice)
            case TurnOutcome.DRAW:
                return next(choice for choice in cls if choice == opponent_choice)
            case TurnOutcome.WIN:
                return next(choice for choice in cls if choice > opponent_choice)

    def __eq__(self, other: PlayerChoice) -> bool:
        return self is other

    def __gt__(self, other: PlayerChoice) -> bool:
        match self, other:
            case self.ROCK, self.SCISSORS:
                return True
            case self.PAPER, self.ROCK:
                return True
            case self.SCISSORS, self.PAPER:
                return True
            case _:
                return False

    def __lt__(self, other: PlayerChoice) -> bool:
        return other > self


TurnChoices = tuple[PlayerChoice, PlayerChoice]
TurnStrategy = tuple[PlayerChoice, TurnOutcome]


def parse_turn_choices(line: str) -> TurnChoices:
    return tuple(PlayerChoice.parse(char) for char in line.split(" "))


def parse_turn_strategy(line: str) -> TurnStrategy:
    choice, strategy = line.split(" ")
    return PlayerChoice.parse(choice), TurnOutcome.parse(strategy)


def turn_choices_from_strategy(strategy: TurnStrategy) -> TurnChoices:
    opponent_choice, outcome = strategy
    return opponent_choice, PlayerChoice.from_opponent_choice(opponent_choice, outcome)


def score_from_turn_choices(turn: TurnChoices) -> int:
    opponent_choice, own_choice = turn
    base_score = own_choice.value
    if own_choice > opponent_choice:  # win
        return base_score + TurnOutcome.WIN.value
    elif own_choice == opponent_choice:  # draw
        return base_score + TurnOutcome.DRAW.value
    else:  # defeat
        return base_score + TurnOutcome.LOSE.value


def total_score_from_turns_choices(turns: Iterable[TurnChoices]) -> int:
    return sum(score_from_turn_choices(turn) for turn in turns)


if __name__ == "__main__":
    turns_choices = parse_input(sep="\n", parse_fn=parse_turn_choices)
    print("Part 1:", total_score_from_turns_choices(turns_choices))
    turns_strategies = parse_input(sep="\n", parse_fn=parse_turn_strategy)
    turns_choices = (turn_choices_from_strategy(s) for s in turns_strategies)
    print("Part 2:", total_score_from_turns_choices(turns_choices))
