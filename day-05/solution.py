from __future__ import annotations

import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import cat, parse_input, transpose

Stack = list[str]  # first element is the bottom of the stack, last is the top
Stacks = dict[str, Stack]
Move = tuple[int, str, str]
MOVE_PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")


def parse_stacks(stacks_input: str) -> Stacks:
    # Stacks are represented vertically, we need a horizontal representation so
    # that each stacks is represented by a single line (not a column)
    lines = transpose(reversed(stacks_input.split("\n")))
    stacks_lines = tuple(
        tuple(char for char in line if char != " ")  # " " is the absence of a crate
        for line in lines
        if str.isdigit(line[0])  # filter out "non-stack" lines
    )
    return {number: crates for (number, *crates) in stacks_lines}


def parse_moves(moves_input: str) -> list[Move]:
    moves_lines = moves_input.split("\n")
    moves = []
    for line in moves_lines:
        count, source, destination = MOVE_PATTERN.match(line).groups()
        moves.append((int(count), source, destination))
    return moves


def move_crates_one_by_one(stacks: Stacks, move: Move) -> Stacks:
    count, source, destination = move
    for _ in range(count):
        crate = stacks[source].pop()
        stacks[destination].append(crate)
    return stacks


def moves_crates_all_at_once(stacks: Stacks, move: Move) -> Stacks:
    count, source, destination = move
    crates = reversed([stacks[source].pop() for _ in range(count)])
    stacks[destination].extend(crates)
    return stacks


def solve_part_1(stacks_input: str, moves_input: str) -> str:
    stacks = parse_stacks(stacks_input)
    moves = parse_moves(moves_input)
    for move in moves:
        stacks = move_crates_one_by_one(stacks, move)
    stacks_tops = cat((s.pop() for s in stacks.values()))
    return stacks_tops


def solve_part_2(stacks_input: str, moves_input: str) -> str:
    stacks = parse_stacks(stacks_input)
    moves = parse_moves(moves_input)
    for move in moves:
        stacks = moves_crates_all_at_once(stacks, move)
    stacks_tops = cat((s.pop() for s in stacks.values()))
    return stacks_tops


if __name__ == "__main__":
    stacks_input, moves_input = parse_input(sep="\n\n")
    print("Part 1:", solve_part_1(stacks_input, moves_input))
    print("Part 2:", solve_part_2(stacks_input, moves_input))
