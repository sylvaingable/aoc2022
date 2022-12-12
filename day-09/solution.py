from __future__ import annotations
from dataclasses import dataclass

import os
import sys
from typing import Iterable

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import assert_never, parse_input, flatten, sliding_window


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def move(self, vector: Vector) -> Point:
        return type(self)(self.x + vector.x, self.y + vector.y)


@dataclass(frozen=True)
class Vector:
    x: int  # horizontal dimension
    y: int  # vertical dimension

    @classmethod
    def from_points(cls, start: Point, end: Point) -> Vector:
        return cls(end.x - start.x, end.y - start.y)

    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def as_tail_move(self) -> Vector:
        """
        Returns a vector whose absolute value in any dimension is less or equal to 1
        """
        return type(self)(normalize_dim(self.x), normalize_dim(self.y))


ORIGIN = Point(0, 0)


def normalize_dim(dim: int) -> int:
    if dim != 0:
        return dim // abs(dim)
    return dim


def motions_vectors_from_line(line: str) -> tuple[Vector]:
    move, count = line.split()
    count = int(count)
    match move:
        case "R":
            vector = Vector(1, 0)
        case "L":
            vector = Vector(-1, 0)
        case "U":
            vector = Vector(0, 1)
        case "D":
            vector = Vector(0, -1)
        case _:
            assert_never(move)
    return tuple(vector for _ in range(count))


def next_tail_position(*, head_pos: Point, tail_pos: Point) -> Point:
    """Next position of the tail given the current head and tail positions"""
    vector = Vector.from_points(tail_pos, head_pos)
    # Head is over or moving around the tail, no need to move the tail
    if sorted(abs(dim) for dim in vector.as_tuple()) in ([0, 0], [0, 1], [1, 1]):
        return tail_pos
    return tail_pos.move(vector.as_tail_move())


def solve_part_1(head_moves: Iterable[Vector]) -> int:
    tail_pos = ORIGIN
    tail_pos_history = {tail_pos}
    # Initially the head covers the tail, let's move it away from the tail.
    head_moves = iter(head_moves)
    head_pos = ORIGIN.move(next(head_moves))
    for vector in head_moves:
        head_pos = head_pos.move(vector)
        tail_pos = next_tail_position(head_pos=head_pos, tail_pos=tail_pos)
        tail_pos_history.add(tail_pos)
    return len(tail_pos_history)


def solve_part_2(head_moves: Iterable[Vector]) -> int:
    knots_pos = [ORIGIN for _ in range(10)]
    tail_pos_history = {knots_pos[-1]}
    head_moves = iter(head_moves)
    # Initially the head covers all the over knots, let's move it away
    knots_pos[0] = knots_pos[0].move(next(head_moves))
    for vector in head_moves:
        knots_pos[0] = knots_pos[0].move(vector)
        # We can move all the other knots by taking them two-by-two and considering
        # the first one as the head and the second one as the tail of the first
        # part.
        for idx, next_idx in sliding_window(range(len(knots_pos)), size=2):
            knots_pos[next_idx] = next_tail_position(
                head_pos=knots_pos[idx], tail_pos=knots_pos[next_idx]
            )
        tail_pos_history.add(knots_pos[-1])
    return len(tail_pos_history)


if __name__ == "__main__":
    head_moves = tuple(flatten(parse_input(parse_fn=motions_vectors_from_line)))
    print("Part 1:", solve_part_1(head_moves))
    print("Part 2:", solve_part_2(head_moves))
