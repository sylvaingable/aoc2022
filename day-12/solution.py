from __future__ import annotations
from dataclasses import dataclass, field

import os
import string
import sys
from rich import print

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import parse_input

Point = tuple[int, int]
Height = int
Distance = int


@dataclass
class Node:
    point: Point
    height: Height
    neighbors: set[Point] = field(default_factory=set)


def parse_height(char: str) -> int:
    match char:
        case "S":
            return 0
        case "E":
            return 27
        case _:
            return string.ascii_lowercase.index(char) + 1


def parse_line(line: str) -> tuple[int]:
    return tuple(parse_height(char) for char in line)


def graph_from_heights(heights_array: tuple[tuple[Height]]) -> dict[Point, Node]:
    """ "
    Transforms the array of heights for each point of the grid into a unweighted
    graph of points reachable from each point.
    """
    graph = {}
    for x, row in enumerate(heights_array):
        for y, height in enumerate(row):
            node = Node(point=(x, y), height=height)
            graph[(x, y)] = node
            if y > 0:
                left_node = graph[(x, y - 1)]
                if abs(node.height - left_node.height) in {0, 1}:
                    node.neighbors.add(left_node.point)
                    left_node.neighbors.add(node.point)
                else:
                    if node.height > left_node.height:
                        node.neighbors.add(left_node.point)
                    else:
                        left_node.neighbors.add(node.point)
            if x > 0:
                upper_node = graph[(x - 1, y)]
                if abs(node.height - upper_node.height) in {0, 1}:
                    node.neighbors.add(upper_node.point)
                    upper_node.neighbors.add(node.point)
                else:
                    if node.height > upper_node.height:
                        node.neighbors.add(upper_node.point)
                    else:
                        upper_node.neighbors.add(node.point)
    return graph


def bfs_shortest_path(
    graph: dict[Point, Node], start: Point, end: Point
) -> list[Point]:
    """
    Finds the shortest path between start and end points in the graph using a
    breadth-first search algorithm (https://www.wikiwand.com/en/Breadth-first_search).
    """
    if start == end:
        return [start]
    queue = [[start, []]]
    visited_points = set()
    while queue:
        next_point, path = queue.pop(0)
        visited_points.add(next_point)
        for neighbor_point in graph[next_point].neighbors:
            if neighbor_point == end:
                return path + [next_point, neighbor_point]
            if neighbor_point in visited_points:
                continue
            neighbor_path = path + [next_point]
            # Don't add a path to the queue if there's already a shorter or equally
            # long path to he same node (we're only interested by the length
            # of the final path between the start and the end nodes.)
            idx, known_path = next(
                (
                    (idx, path)
                    for idx, (point, path) in enumerate(queue)
                    if point == neighbor_point
                ),
                (None, []),
            )
            if idx is not None and len(known_path) <= len(neighbor_path):
                continue
            queue.append([neighbor_point, neighbor_path])
    return []


def solve_part_1(heights_array: tuple[tuple[Height]]) -> int:
    graph = graph_from_heights(heights_array)
    start_point = next(point for point, vertex in graph.items() if vertex.height == 0)
    end_point = next(point for point, vertex in graph.items() if vertex.height == 27)
    shortest_path = bfs_shortest_path(graph, start_point, end_point)
    return len(shortest_path) - 1


def solve_part_2(heights_array: tuple[tuple[Height]]) -> int:
    graph = graph_from_heights(heights_array)
    end_point = next(point for point, vertex in graph.items() if vertex.height == 27)
    start_points = tuple(point for point, vertex in graph.items() if vertex.height == 1)
    paths_lengths = tuple(
        len(bfs_shortest_path(graph, start_point, end_point)) - 1
        for start_point in start_points
    )
    # The end point cannot be reached from some start points, the corresponding
    # paths are empty and must be excluded
    return min(l for l in paths_lengths if l > 0)


if __name__ == "__main__":
    heights_array = parse_input(parse_fn=parse_line)
    print("Part 1:", solve_part_1(heights_array))
    print("Part 2:", solve_part_2(heights_array))
