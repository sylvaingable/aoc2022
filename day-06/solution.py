from __future__ import annotations

import os
import sys
from typing import Generator, Optional

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import parse_input

START_PACKET_LENGTH = 4
START_MESSAGE_LENGTH = 14


def sliding_window(input: str, size: int = 1) -> Generator[str, None, None]:
    for i in range(0, len(input) - size):
        yield input[i : i + size]


def are_chars_uniques(chars: str) -> bool:
    return len(set(chars)) == len(chars)


def solve_part_1(data_stream: str) -> Optional[int]:
    for i, chars in enumerate(sliding_window(data_stream, size=START_PACKET_LENGTH)):
        if are_chars_uniques(chars):
            return i + START_PACKET_LENGTH


def solve_part_2(data_stream: str) -> Optional[int]:
    for i, chars in enumerate(sliding_window(data_stream, size=START_MESSAGE_LENGTH)):
        if are_chars_uniques(chars):
            return i + START_MESSAGE_LENGTH


if __name__ == "__main__":
    data_stream, *_ = parse_input()
    print("Part 1:", solve_part_1(data_stream))
    print("Part 2:", solve_part_2(data_stream))
