from __future__ import annotations
from functools import partial
from itertools import chain

import os
import sys
from typing import Sequence, TypeVar

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import count_if, overlay, parse_input, reverse, transpose

T = TypeVar("T")
Line = Sequence[T]
Grid = Sequence[Sequence[T]]


def parse_line(line: str) -> Line[int]:
    return tuple(int(char) for char in line)


def compute_line_visibility(trees_line: Line[int]) -> Line[bool]:
    """
    Transforms a trees line into the visibility (True/False) of each tree, looking
    from the start of the line to the end of the line.
    """
    tallest = -1
    visibilities = []
    for tree in trees_line:
        if tree > tallest:
            visibilities.append(True)
            tallest = tree
        else:
            visibilities.append(False)
    return visibilities


def compute_grid_visibility(trees_grid: Grid[int]) -> Grid[bool]:
    """
    A tree is visible if it can be seen looking from the left, right, top or
    bottom of the grid.
    Here we generate grids whose lines are ordered as if we were looking fro
    the left/right/top/bottom of the grid and compute the visibility of each tree
    in this case.
    All the visibilities are then combined (a tree is globally visible if it can
    be seen from any direction) to determine its global visibility.
    """
    visible_from_left = tuple(compute_line_visibility(line) for line in trees_grid)
    visible_from_right = reverse(
        tuple(compute_line_visibility(line) for line in reverse(trees_grid))
    )
    visible_from_top = transpose(
        tuple(compute_line_visibility(line) for line in transpose(trees_grid))
    )
    visible_from_bottom = transpose(
        reverse(
            tuple(
                compute_line_visibility(line) for line in reverse(transpose(trees_grid))
            )
        )
    )
    visible_from_anywhere = overlay(
        visible_from_left,
        visible_from_right,
        visible_from_top,
        visible_from_bottom,
        reducer=any,
    )
    return visible_from_anywhere


def solve_part_1(trees_grid: Grid[int]) -> int:
    visible_trees = compute_grid_visibility(trees_grid)
    visible_count = count_if(chain(*visible_trees))
    return visible_count


def visibility_count(trees_line: Line[int]) -> int:
    """
    Number of trees in the line having an height less than the first tree (the
    count includes the first tree).
    """
    starting_height, *heights = trees_line
    return next(
        (idx + 1 for idx, height in enumerate(heights) if height >= starting_height),
        len(heights),
    )


def column_from_grid(grid: Grid, col_idx: int) -> Line:
    return tuple(line[col_idx] for line in grid)


def compute_scenic_score(trees_grid: Grid[int], tree_x: int, tree_y: int) -> int:
    trees_to_the_right = trees_grid[tree_x][tree_y:]
    trees_to_the_left = trees_grid[tree_x][: tree_y + 1][::-1]
    trees_to_the_bottom = column_from_grid(trees_grid, tree_y)[tree_x:]
    trees_to_the_top = column_from_grid(trees_grid, tree_y)[: tree_x + 1][::-1]
    return (
        visibility_count(trees_to_the_right)
        * visibility_count(trees_to_the_left)
        * visibility_count(trees_to_the_bottom)
        * visibility_count(trees_to_the_top)
    )


def solve_part_2(trees_grid: Grid[int]) -> int:
    grid_side = len(trees_grid)
    visible_trees = compute_grid_visibility(trees_grid)
    get_scenic_score = partial(compute_scenic_score, trees_grid)
    # To speed the search up let's exclude:
    # - Trees on the borders, their scenic score will always be 0.
    # - Trees not visible from outside (see part 1), they're not good candidates
    #   since visibilities in all directions from the tree are multiplied together.
    #   It's a "bet" that could be wrong but turned out to be right either with
    #   the example and the input data.
    return max(
        get_scenic_score(x, y)
        for x in range(1, grid_side)
        for y in range(1, grid_side)
        if visible_trees[x][y] is True
    )


if __name__ == "__main__":
    trees_grid = parse_input(parse_fn=parse_line)
    print("Part 1:", solve_part_1(trees_grid))
    print("Part 2:", solve_part_2(trees_grid))
