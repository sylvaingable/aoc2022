from __future__ import annotations
from itertools import chain

import os
import sys
from typing import Generator
from rich import print

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import (  # noqa: E402
    batchify,
    flatten,
    parse_input,
    parse_ints,
    Point,
    X,
    Y,
)


def parse_line(line: str) -> tuple[Point, Point]:
    return tuple(tuple(el) for el in batchify(parse_ints(line), batch_size=2))


def manhattan_distance(point: Point, other_point: Point) -> int:
    return abs(X(point) - X(other_point)) + abs(Y(point) - Y(other_point))


def sensor_range(sensor: Point, closest_beacon: Point) -> int:
    return manhattan_distance(sensor, closest_beacon)


def is_in_range(loc: Point, sensor_loc: Point, sensor_range: int) -> int:
    return manhattan_distance(loc, sensor_loc) <= sensor_range


def sensor_border(sensor: Point, s_range: int) -> Generator[Point, None, None]:
    x_range = range(-s_range, s_range + 1)
    y_range = chain(range(0, s_range), range(s_range, -1, -1))
    for x, y in zip(x_range, y_range):
        yield (X(sensor) + x, Y(sensor) + y)
        if abs(Y(sensor)) != (abs(y)):
            yield (X(sensor) + x, Y(sensor) - y)


def solve_part_1(sensors_and_beacons: tuple[tuple[Point, Point]], row_idx: int) -> int:
    # Locations where sensors or beacons are already present must not be considered
    ignored_locations = set(
        loc for loc in flatten(sensors_and_beacons) if Y(loc) == row_idx
    )
    # Discard sensors that are vertically too far away (i.e. their range don't allow
    # them to reach the row we're searching).
    candidate_sensors = tuple(
        (sensor, sensor_range(sensor, beacon))
        for sensor, beacon in sensors_and_beacons
        if abs(Y(sensor) - row_idx) <= sensor_range(sensor, beacon)
    )
    # Determine the locations along the row we are searching that can be reached by
    # any candidate sensor. Since we need to keep track of the locations (a single
    # location could be reached by multiple sensors) it's less memory efficient than
    # iterating over all the locations in the row but a bit faster.
    excluded_locations = set()
    for s_loc, s_range in candidate_sensors:
        excluded_locations.update(
            (x, row_idx)
            for x in range(
                X(s_loc) - (s_range - abs(Y(s_loc) - row_idx)),
                X(s_loc) + (s_range - abs(Y(s_loc) - row_idx)) + 1,
            )
            if (x, row_idx) not in ignored_locations
        )
    return len(excluded_locations)


def solve_part_2(
    sensors_and_beacons: tuple[tuple[Point, Point]], search_range: int
) -> int | None:
    excluded_locations = set(
        loc
        for loc in flatten(sensors_and_beacons)
        if 0 <= X(loc) <= search_range and 0 <= Y(loc) <= search_range
    )
    # Since the location we're looking for is the only one not in range of any sensor
    # it can only be next to a sensor's border (otherwise there would be several
    # locations not in range).
    for idx, (s_loc, b_loc) in enumerate(sensors_and_beacons, start=1):
        print(f"Processing sensor {idx}/{len(sensors_and_beacons)}")
        distress_beacon_location = next(
            (
                loc
                for loc in sensor_border(s_loc, sensor_range(s_loc, b_loc) + 1)
                if loc not in excluded_locations
                and 0 <= X(loc) <= search_range
                and 0 <= Y(loc) <= search_range
                and not any(
                    is_in_range(loc, s_loc, sensor_range(s_loc, b_loc))
                    for s_loc, b_loc in sensors_and_beacons
                )
            ),
            None,
        )
        if distress_beacon_location is not None:
            return X(distress_beacon_location) * 4_000_000 + Y(distress_beacon_location)


if __name__ == "__main__":
    sensors_and_beacons = parse_input(parse_fn=parse_line)
    print("Part 1:", solve_part_1(sensors_and_beacons, row_idx=2_000_000))
    print("Part 2:", solve_part_2(sensors_and_beacons, search_range=4_000_000))
