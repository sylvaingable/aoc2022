from __future__ import annotations

import re
from itertools import chain
from typing import (
    Any,
    Callable,
    Container,
    Generator,
    Hashable,
    Iterable,
    Protocol,
    Sequence,
    TypeVar,
)

T = TypeVar("T")
INT_REGEX = re.compile(r"(-*\d+)")


def parse_input(
    path: str = "./input", sep: str = "\n", parse_fn: Callable[[str], T] = str
) -> tuple[T, ...]:
    """Returns parsed lines from an input file."""
    with open(path, "r") as f:
        lines = f.read().rstrip().split(sep)
        return tuple(parse_fn(line) for line in lines)


def parse_ints(text: str) -> tuple[int, ...]:
    return tuple(int(m) for m in INT_REGEX.findall(text))


def assert_never(value):
    """
    Raises an AssertionError for the provided value.

    It should be use when matching against known values to raise an exception
    for unexpected values (typically in a final else clause).
    """
    raise AssertionError(f"Unhandled value: {value}")


###################
# Iteration utils #
###################


def batchify(iterable: Iterable[T], batch_size: int) -> Generator[list[T], None, None]:
    """
    Yields batches of batch_size from the iterable. The last batch will be
    smaller than batch_size if the iterable length isn't a multiple of batch_size.
    E.g.:
    >>> tuple(batchify(iterable=[1, 2, 3], batch_size=2))
    ([1,2], [3])
    """
    iterator, cursor = iter(iterable), 0
    batch = []
    while True:
        try:
            batch.append(next(iterator))
            cursor += 1
        except StopIteration:
            if batch:
                yield batch
            return
        if cursor % batch_size == 0:
            yield batch
            batch = []


def count_if(iterable: Iterable, predicate: Callable[[Any], bool] = bool) -> int:
    """Counts the number of elements from the iterable matching the predicate."""
    return sum(1 for el in iterable if predicate(el))


def cat(iterable: Iterable[str]) -> str:
    return "".join(str(el) for el in iterable)


def first(iterable: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(iterable), default)


def last(seq: Sequence[T], default: T | None = None) -> T | None:
    return next(reversed(seq), default)


flatten = chain.from_iterable


def sliding_window(
    iterable: Iterable[T], size: int = 1
) -> Generator[tuple[T, ...], None, None]:
    iterator = iter(iterable)
    try:
        window = tuple(next(iterator) for _ in range(size))
    except RuntimeError:
        raise ValueError("size must be less than or equal to iterable length")
    yield window
    for next_element in iterator:
        window = window[1:] + (next_element,)
        yield window


###########################
# Array-related functions #
###########################


def transpose(array: Sequence[Sequence[T]]) -> tuple[tuple[T]]:
    return tuple(zip(*array))


def reverse(array: Sequence[Sequence[T]]) -> tuple[tuple[T]]:
    return tuple(tuple(reversed(line)) for line in array)


def overlay(
    *arrays: Sequence[Sequence[T]], reducer: Callable[[Iterable[T]], T]
) -> tuple[tuple[T]]:
    """
    Merges arrays of identical size in single one, reducing values at the position
    with the reducer function.
    E.g.:
    >>> overlay([[1, 2], [3, 4]], [[1, 2], [3, 4]], reducer=sum)
    ((2, 4), (6, 8))
    """
    return tuple(
        tuple(reducer(values) for values in zip(*merged_lines))
        for merged_lines in zip(*arrays)
    )


################################
# Point/Grid related functions #
################################

Point = tuple[int, int]


def X(point: Point) -> int:
    return point[0]


def Y(point: Point) -> int:
    return point[1]


############################
# Graphs related functions #
############################


class Node(Protocol):
    neighbors: Iterable[Node]


Graph = dict[Hashable, Node]


def bfs_shortest_path(graph: Graph, start: Hashable, end: Hashable) -> list[Hashable]:
    """
    Finds the shortest path between start and end nodes in the graph using a
    breadth-first search algorithm (https://www.wikiwand.com/en/Breadth-first_search).
    """
    if start == end:
        return [start]
    queue = [[start, []]]
    visited = set()
    while queue:
        next_node, path = queue.pop(0)
        visited.add(next_node)
        for neighbor in graph[next_node].neighbors:
            if neighbor == end:
                return path + [next_node, neighbor]
            if neighbor in visited:
                continue
            neighbor_path = path + [next_node]
            # Don't add a path to the queue if there's already a shorter or equally
            # long path to he same node (we're only interested by the length
            # of the final path between the start and the end nodes.)
            idx, known_path = next(
                (
                    (idx, path)
                    for idx, (point, path) in enumerate(queue)
                    if point == neighbor
                ),
                (None, []),
            )
            if idx is not None and len(known_path) <= len(neighbor_path):
                continue
            queue.append([neighbor, neighbor_path])
    return []
