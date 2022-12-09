from itertools import chain
from typing import Any, Callable, Generator, Iterable, TypeVar

T = TypeVar("T")


def parse_input(
    path: str = "./input", sep: str = "\n", parse_fn: Callable[[str], T] = str
) -> tuple[T, ...]:
    """Returns parsed lines from an input file."""
    with open(path, "r") as f:
        lines = f.read().rstrip().split(sep)
        return tuple(parse_fn(line) for line in lines)


def batchify(iterable: Iterable, batch_size: int) -> Generator[list, None, None]:
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


def transpose(array) -> tuple:
    return tuple(zip(*array))


def cat(iterable: Iterable[str]) -> str:
    return "".join(str(el) for el in iterable)


flatten = chain.from_iterable
