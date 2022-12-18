from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce

import os
import re
import sys
from operator import add, mul
from rich import print
from typing import Callable

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import assert_never, parse_input


Item = int
MonkeyId = int

MONKEY_REGEX = re.compile(
    r"""Monkey (\d+):
  Starting items: (.+)
  Operation: new = old (.) (.+)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)"""
)


@dataclass
class Monkey:
    mid: MonkeyId
    items: list[Item]
    divisor: int
    inspector: Callable[[Item], Item]
    tester: Callable[[Item], MonkeyId]


def make_inspector(operator: str, operand: str) -> Callable[[Item], Item]:
    match operator:
        case "*":
            op = mul
        case "+":
            op = add
        case _:
            assert_never(operator)

    match operand:
        case "old":
            return lambda item: op(item, item)
        case _:
            return lambda item: (op(item, int(operand)))


def make_tester(
    divisor: int, truthy_mid: MonkeyId, falsy_mid: MonkeyId
) -> Callable[[Item], MonkeyId]:
    return lambda item: truthy_mid if item % divisor == 0 else falsy_mid


def parse_monkey(text_desc: str) -> Monkey:
    match = MONKEY_REGEX.match(text_desc)
    if not match:
        raise ValueError("Cannot parse data")
    mid, items, operator, operand, divisor, truthy_mid, falsy_mid = match.groups()
    return Monkey(
        mid=int(mid),
        items=[int(el) for el in items.split(", ")],
        divisor=int(divisor),
        inspector=make_inspector(operator, operand),
        tester=make_tester(int(divisor), int(truthy_mid), int(falsy_mid)),
    )


def solve_part_1(monkeys: tuple[Monkey, ...]) -> int:
    seen_items_counts = defaultdict(lambda: 0)
    for _ in range(20):
        for monkey in monkeys:
            while len(monkey.items):
                item = monkey.items.pop(0)
                seen_items_counts[monkey.mid] += 1
                item = monkey.inspector(item) // 3
                next_mid = monkey.tester(item)
                monkeys[next_mid].items.append(item)
    return mul(*sorted(seen_items_counts.values(), reverse=True)[:2])


def solve_part_2(monkeys: tuple[Monkey, ...]) -> int:
    seen_items_counts = defaultdict(lambda: 0)
    # The same implementation as in part 1 doesn't complete in a reasonable time
    # since items values become very high and it takes more and more to time to
    # add/multiply/divide them.
    # Since we only need to know whether items are divisible by each monkey divisor
    # to decide which monkey to throw the item next, we can keep the remainder of
    # their division by a common multiple to all divisors to prevent items values
    # going too high while keeping their "divisibility" characteristic.
    common_divisors_multiple = reduce(mul, (m.divisor for m in monkeys))
    for _ in range(10_000):
        for monkey in monkeys:
            while len(monkey.items):
                item = monkey.items.pop(0)
                seen_items_counts[monkey.mid] += 1
                item = monkey.inspector(item) % common_divisors_multiple
                next_mid = monkey.tester(item)
                monkeys[next_mid].items.append(item)
    return mul(*sorted(seen_items_counts.values(), reverse=True)[:2])


if __name__ == "__main__":
    monkeys = parse_input(sep="\n\n", parse_fn=parse_monkey)
    print("Part 1:", solve_part_1(monkeys))
    # Monkeys items lists were mutated in part 1, re-initialize them
    monkeys = parse_input(sep="\n\n", parse_fn=parse_monkey)
    print("Part 2:", solve_part_2(monkeys))
