from __future__ import annotations
from functools import cmp_to_key, reduce
from operator import mul

import os
import sys
from rich import print

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import parse_input, flatten

DIVIDER_PACKETS = ([[2]], [[6]])


def parse_packets_pair(two_lines: str) -> tuple[list, list]:
    first_line, second_line = two_lines.split("\n")
    # eval should not be used against arbitrary input but it's safe here
    return eval(first_line), eval(second_line)


def are_packets_in_order(left_packet: list, right_packet: list) -> bool | None:
    """
    Returns True if packets are in the right order, False otherwise and None if
    the packets ordering cannot be determined.
    """
    for left, right in zip(left_packet, right_packet):
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True
            if left > right:
                return False
        if isinstance(left, list) and isinstance(right, list):
            comparison = are_packets_in_order(left, right)
            if comparison is not None:
                return comparison
        if isinstance(left, int) ^ isinstance(right, int):
            left = [left] if isinstance(left, int) else left
            right = [right] if isinstance(right, int) else right
            comparison = are_packets_in_order(left, right)
            if comparison is not None:
                return comparison
    # As a last resort, packets are ordered if left is shorter than right
    if len(left_packet) != len(right_packet):
        return len(left_packet) < len(right_packet)


def compare_packets(first: list, second: list) -> int:
    """
    Comparison functions for packers order that can be used by Python built-in
    sorting functions.
    """
    match are_packets_in_order(first, second):
        case True:
            return -1
        case None:
            return 0
        case False:
            return 1


def solve_part_1(packets_pairs: tuple[tuple[list, list]]) -> int:
    are_packets_ordered = tuple(are_packets_in_order(*pair) for pair in packets_pairs)
    return sum(
        idx
        for idx, predicate in enumerate(are_packets_ordered, start=1)
        if predicate is True
    )


def solve_part_2(packets_pairs: tuple[tuple[list, list]]) -> int:
    packets = tuple(flatten(packets_pairs)) + DIVIDER_PACKETS
    sorted_packets = sorted(packets, key=cmp_to_key(compare_packets))
    return reduce(
        mul,
        (idx for idx, p in enumerate(sorted_packets, start=1) if p in DIVIDER_PACKETS),
    )


if __name__ == "__main__":
    packets_pairs = parse_input(sep="\n\n", parse_fn=parse_packets_pair)
    print("Part 1:", solve_part_1(packets_pairs))
    print("Part 2:", solve_part_2(packets_pairs))
