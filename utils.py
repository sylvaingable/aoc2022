from typing import Any, Callable


def parse_input(
    path: str = "./input", sep: str = "\n", parse_fn: Callable[[str], Any] = str
) -> tuple:
    """Returns parsed lines from an input file."""
    with open(path, "r") as f:
        lines = f.read().rstrip().split(sep)
        return tuple(parse_fn(line) for line in lines)
