import os
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import parse_input


Snack = tuple[int, ...]


def parse_snacks(line: str) -> Snack:
    return tuple(int(w) for w in line.split("\n"))


def calories_from_snack(snack: Snack) -> int:
    return sum(snack)


def greatest_total_calories(snacks: tuple[Snack]) -> int:
    return max(calories_from_snack(snack) for snack in snacks)


def top_three_total_calories(snacks: tuple[Snack]) -> int:
    snacks_calories = tuple(calories_from_snack(snack) for snack in snacks)
    return sum(sorted(snacks_calories, reverse=True)[:3])


if __name__ == "__main__":
    data = parse_input(sep="\n\n", parse_fn=parse_snacks)
    print("Part 1:", greatest_total_calories(data))
    print("Part 2:", top_three_total_calories(data))
