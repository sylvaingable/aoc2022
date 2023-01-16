from __future__ import annotations
import copy
from functools import partial, reduce
from itertools import permutations
from operator import itemgetter

import re
import os
import sys
from typing import NamedTuple
from rich import print

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import (  # noqa: E402
    assert_never,
    bfs_shortest_path,
    first,
    parse_input,
    sliding_window,
)

Valve = NamedTuple("Valve", [("flow", int), ("neighbors", set[str])])
ValvesGraph = dict[str, Valve]

LINE_PATTERN = re.compile(
    r"""Valve ([A-Z]{2}) has flow rate=(\d+); tunnels* leads* to valves* (.+)"""
)


def parse_line(line: str) -> tuple[str, Valve]:
    if (match := LINE_PATTERN.match(line)) is not None:
        valve, flow, neighbor_valves = match.groups()
        return valve, Valve(flow=int(flow), neighbors=set(neighbor_valves.split(", ")))
    assert_never(line)


def compute_total_pressure_released(
    graph: ValvesGraph, paths: dict[tuple[str, str], int], steps: list[str]
) -> int:
    openings = []
    remaining_time = 30
    for v_from, v_to in sliding_window(steps, size=2):
        remaining_time -= paths[(v_from, v_to)]
        openings.append((remaining_time, graph[v_to].flow))
    return sum(time * flow for time, flow in openings if time > 0)


def solve_part_1(valves_graph: ValvesGraph) -> int:
    shortest_path = partial(bfs_shortest_path, valves_graph)

    valves_of_interest = tuple(
        key for key, value in valves_graph.items() if value.flow != 0
    )
    print("Valves with flow > 0:", len(valves_of_interest))
    paths_of_interest: dict[tuple[str, str], int] = {}
    for start, end in permutations(("AA",) + valves_of_interest, r=2):
        distance = len(shortest_path(start, end))
        paths_of_interest |= {(start, end): distance, (end, start): distance}
    print(
        sorted(
            (start, end, dist, valves_graph[end].flow)
            for (start, end), dist in paths_of_interest.items()
        )
    )

    total_pressure_released = partial(
        compute_total_pressure_released, valves_graph, paths_of_interest
    )
    steps = ["AA"]
    for _ in range(len(valves_of_interest)):
        curr_valve = steps[-1]
        next_valve = first(
            sorted(
                (
                    end
                    for (start, end), distance in paths_of_interest.items()
                    if start == curr_valve and end not in steps
                ),
                key=lambda v: paths_of_interest[(curr_valve, v)],
            ),
        )
        steps.append(next_valve)
    print(steps)
    released_pressure = total_pressure_released(steps)

    for idx, _ in enumerate(steps[1:]):
        for next_idx, _ in enumerate(steps[idx:]):
            alternate_steps = copy.copy(steps)
            alternate_steps[idx], alternate_steps[next_idx] = (
                alternate_steps[next_idx],
                alternate_steps[idx],
            )
            if total_pressure_released(alternate_steps) > released_pressure:
                steps = alternate_steps
                released_pressure = alternate_steps
                break

    print(steps)
    return released_pressure

    # distances = sorted(paths_of_interest.values())[::2]
    # max_steps = next(i - 1 for i in range(1, len(distances)) if sum(distances[:i]) > 30)
    # print("Max steps:", max_steps)

    # possible_steps = (
    #     ("AA",) + faster_steps
    #     for faster_steps in permutations(
    #         valves_of_interest, r=min(len(valves_of_interest), max_steps)
    #     )
    # )
    # return max(total_pressure_released(faster_steps) for faster_steps in possible_steps)
    # A > D > B > J > H > E > C


def solve_part_2():
    pass


if __name__ == "__main__":
    valves_graph = dict(parse_input(parse_fn=parse_line))
    print("Part 1:", solve_part_1(valves_graph))
    # print("Part 2:", solve_part_2(sensors_and_beacons, search_range=4_000_000))
