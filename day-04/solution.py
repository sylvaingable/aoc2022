from __future__ import annotations

import os
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import count_if, parse_input

Assignment = tuple[int, int]
AssignmentsPair = tuple[Assignment, Assignment]


def parse_assignments_pair(line: str) -> AssignmentsPair:
    return tuple(
        tuple(int(section) for section in assignment.split("-"))
        for assignment in line.split(",")
    )


def are_pairs_inclusive(assignments_pair: AssignmentsPair) -> bool:
    (first_start, first_end), (second_start, second_end) = assignments_pair
    # Pairs are inclusive if
    return (
        # The first pair is contained by the second pair
        (first_start >= second_start and first_end <= second_end)
        # The second pair is contained by the first pair
        or (second_start >= first_start and second_end <= first_end)
    )


def do_pairs_overlap(assignments_pair: AssignmentsPair) -> bool:
    (first_start, first_end), (second_start, second_end) = assignments_pair
    # Pairs overlap if they're not fully separated, i.e.:
    return (
        # The first pair is not before the second pair
        not first_end < second_start
        # The first pair is not after second pair
        and not first_start > second_end
    )


def solve_part_1(pairs: tuple[Assignment, ...]) -> int:
    return count_if(pairs, predicate=are_pairs_inclusive)


def solve_part_2(pairs: tuple[Assignment, ...]) -> int:
    return count_if(pairs, predicate=do_pairs_overlap)


if __name__ == "__main__":
    assignments_pairs = parse_input(parse_fn=parse_assignments_pair)
    print("Part 1:", solve_part_1(assignments_pairs))
    print("Part 2:", solve_part_2(assignments_pairs))
