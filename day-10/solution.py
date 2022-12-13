from __future__ import annotations
from functools import partial

import os
import sys
from operator import add
from rich import print
from typing import Callable

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import assert_never, flatten, parse_input

RegisterUpdater = Callable[[int], int]
identity = lambda x: x
BLANK_CRT_ROW = "." * 40


def parse_instruction(line: str) -> tuple[RegisterUpdater, ...]:
    """
    Returns tuple of functions that take a register value as its single argument
    and returns its updated value.
    """
    if line.startswith("noop"):
        return (identity,)
    elif line.startswith("addx"):
        _, value = line.split()
        # Decompose the addx instructions in two, matching the two cycles it
        # takes to execute:
        # - A first one that does nothing
        # - A second one that updates the register with the addx argument value
        return (identity, partial(add, int(value)))
    else:
        assert_never(line)


def solve_part_1(instructions: tuple[RegisterUpdater, ...]) -> int:
    register = 1
    compute_signal_strength = lambda cycle, register: cycle * register
    signal_strengths = []
    for cycle, register_updater in enumerate(instructions, start=1):
        if cycle in {20, 60, 100, 140, 180, 220}:
            signal_strengths.append(compute_signal_strength(cycle, register))
        register = register_updater(register)
    return sum(signal_strengths)


def solve_part_2(instructions) -> list[str]:
    register = 1
    sprite = (0, 1, 2)
    crt_row = BLANK_CRT_ROW
    crt_screen = []
    for cycle, register_updater in enumerate(instructions):
        pixel = cycle % 40
        # Add row to screen once fully drawn
        if cycle > 0 and pixel == 0:
            crt_screen.append(crt_row)
            crt_row = BLANK_CRT_ROW
        if pixel in sprite:
            crt_row = crt_row[:pixel] + "#" + crt_row[pixel + 1 :]
        register = register_updater(register)
        sprite = (register - 1, register, register + 1)
    crt_screen.append(crt_row)
    return crt_screen


if __name__ == "__main__":
    instructions = tuple(flatten(parse_input(parse_fn=parse_instruction)))
    print("Part 1:", solve_part_1(instructions))
    print("Part 2:", solve_part_2(instructions))
