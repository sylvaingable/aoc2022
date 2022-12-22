from __future__ import annotations
from functools import partial
from itertools import count

import os
import sys
from typing import Generator, Iterable
from rich import print

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import (  # noqa: E402
    batchify,
    cat,
    flatten,
    parse_input,
    parse_ints,
    Point,
    sliding_window,
    X,
    Y,
)


AIR = "."
ROCK = "#"
SAND = "o"
Scan = dict[int, dict[int, str]]
SAND_SOURCE: Point = (500, 0)


def print_scan(scan: Scan):
    """Prints the scan in the same way as the instructions."""
    height = scan_height(scan)
    for row_idx in range(height + 1):
        print(cat(scan[col_idx].get(row_idx, AIR) for col_idx in sorted(scan.keys())))


def parse_line(line: str) -> tuple[Point]:
    return tuple(tuple(b) for b in batchify(parse_ints(line), batch_size=2))


def points_from_paths(paths: tuple[Point]) -> Generator[Point, None, None]:
    for start, end in sliding_window(paths, size=2):
        if X(start) == X(end):
            min_y, max_y = sorted((Y(start), Y(end)))
            for y in range(min_y, max_y + 1):
                yield (X(start), y)
        if Y(start) == Y(end):
            min_x, max_x = sorted((X(start), X(end)))
            for x in range(min_x, max_x + 1):
                yield (x, Y(start))


def scan_height(scan: Scan) -> int:
    return max(flatten(line.keys() for line in scan.values()))


def init_scan(rock_points: Iterable[Point], add_ground: bool = False) -> Scan:
    """
    Stores the scan "horizontally" as a dict of lines (each line corresponds to
    a vertical slice of the instructions), each line being a dict itself storing
    only the positions of rocks and sands (not air).
    Storing positions as dicts instead of lists/tuples is more memory-efficient
    but the dicts keys need to be sorted first when the order is necessary.
    """
    scan = {}
    for point in rock_points:
        scan.setdefault(X(point), {})[Y(point)] = ROCK
    if add_ground:
        height = scan_height(scan)
        for line in scan.values():
            line[height + 2] = ROCK
    return scan


def landing_point(scan: Scan, x: int, y: int = 0) -> Point:
    """
    Returns the point a sand particle lands on after being dropped from the provided
    coordinates.
    """
    return (x, min((k for k in scan.get(x, {}).keys() if k > y), default=0) - 1)


def roll_down(scan: Scan, from_point: Point) -> Point:
    """
    Starting from point, try going down first on the left then on the right and
    starts again from the next point until it's not possible to go down anymore.
    """
    left_point = landing_point(scan, X(from_point) - 1, Y(from_point))
    if Y(left_point) == -1:
        return left_point
    if Y(left_point) > Y(from_point):
        return roll_down(scan=scan, from_point=left_point)
    right_point = landing_point(scan, X(from_point) + 1, Y(from_point))
    if Y(right_point) == -1:
        return right_point
    if Y(right_point) > Y(from_point):
        return roll_down(scan=scan, from_point=right_point)
    return from_point


def next_point(scan: Scan):
    return roll_down(scan, from_point=landing_point(scan, x=X(SAND_SOURCE)))


def is_off_limits(scan: Scan, point: Point) -> bool:
    return Y(point) < 0 or X(point) < min(scan.keys()) or X(point) > max(scan.keys())


def solve_part_1(paths_list: tuple[tuple[Point]]) -> int:
    rock_points = flatten(points_from_paths(paths) for paths in paths_list)
    scan = init_scan(rock_points)
    find_next_point = partial(next_point, scan)
    is_falling_into_abyss = partial(is_off_limits, scan)
    step = 0  # for type inference
    # Let's start from 0 as we need to know the number of units of sand have
    # come to rest before the sand starts falling into the abyss.
    for step in count(0):
        next_sand_point = find_next_point()
        if is_falling_into_abyss(next_sand_point):
            break
        scan[X(next_sand_point)][Y(next_sand_point)] = SAND
    return step


def solve_part_2(paths_list: tuple[tuple[Point]]) -> int:
    rock_points = flatten(points_from_paths(paths) for paths in paths_list)
    scan = init_scan(rock_points, add_ground=True)
    find_next_point = partial(next_point, scan)
    more_ground_needed = partial(is_off_limits, scan)
    step = 0  # for type inference
    # Let's start from 1 as we need to know how many sand units have come to rest
    # before the source becomes blocked.
    for step in count(1):
        next_sand_point = find_next_point()
        if more_ground_needed(next_sand_point):
            # Let's add some ground as the limits are pushed further
            height = scan_height(scan)
            scan.setdefault(X(next_sand_point), {})[height] = ROCK
            scan[X(next_sand_point)][height - 1] = SAND
            continue
        scan[X(next_sand_point)][Y(next_sand_point)] = SAND
        if next_sand_point == SAND_SOURCE:
            break
    return step


if __name__ == "__main__":
    paths_list = parse_input(parse_fn=parse_line)
    print("Part 1:", solve_part_1(paths_list))
    print("Part 2:", solve_part_2(paths_list))
