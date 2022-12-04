from __future__ import annotations

import os
import string
import sys
from typing import Generator, Iterable

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import batchify, parse_input

Rucksack = tuple[str, ...]
RucksackContent = set[str]
RucksackCompartments = tuple[RucksackContent, RucksackContent]


ITEMS_PRIORITIES = tuple(string.ascii_letters)


def split_rucksack_content(line: str) -> tuple[RucksackContent, RucksackContent]:
    items = tuple(line)
    return set(items[: len(items) // 2]), set(items[len(items) // 2 :])


def yield_groups(
    lines: tuple[Rucksack, ...]
) -> Generator[tuple[RucksackContent, ...], None, None]:
    for group in batchify(lines, batch_size=3):
        yield tuple(set(line) for line in group)


def find_common_item(sets: Iterable[RucksackContent]) -> str:
    head, *tail = sets
    for s in tail:
        head = head.intersection(s)
    return next(iter(head))


def priority_from_item(item: str) -> int:
    return ITEMS_PRIORITIES.index(item) + 1


def solve_part_1(rucksacks_contents: tuple[RucksackCompartments]) -> int:
    common_items = (find_common_item(content) for content in rucksacks_contents)
    priorities_sum = sum(priority_from_item(item) for item in common_items)
    return priorities_sum


def solve_part_2(rucksacks: tuple[Rucksack]) -> int:
    common_items = (find_common_item(group) for group in yield_groups(rucksacks))
    priorities_sum = sum(priority_from_item(item) for item in common_items)
    return priorities_sum


if __name__ == "__main__":
    rucksacks_contents = parse_input(parse_fn=split_rucksack_content)
    print("Part 1:", solve_part_1(rucksacks_contents))
    all_rucksacks = parse_input(parse_fn=tuple)
    print("Part 2:", solve_part_2(all_rucksacks))
