from __future__ import annotations
from dataclasses import dataclass, field
from operator import attrgetter

import re
import os
import sys
from typing import Union

sys.path.append(os.path.abspath(os.path.join("..")))

from utils import flatten, parse_input

Command = tuple[str, list[str]]

LS_FILE_PATTERN = re.compile(r"(\d+)\s(\S+)")
LS_DIR_PATTERN = re.compile(r"dir\s(\S+)")
DIRECTORY_SIZE_THRESHOLD = 100_000
TOTAL_DISK_SPACE = 70_000_000
MIN_FREE_SPACE = 30_000_000


def parse_terminal_command(terminal_output: str) -> Command:
    command, *output = terminal_output.split("\n")
    return command, output


@dataclass
class File:
    size: int


@dataclass
class Directory:
    parent: Directory | None = None
    children: dict[str, Union[File, Directory]] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return sum((child.size for child in self.children.values()), 0)

    def get_child_dir(self, name: str) -> Directory:
        child = self.children[name]
        if not isinstance(child, Directory):
            raise KeyError("Child directory not found")
        return child

    def get_dirs_tree(self) -> tuple[Directory, ...]:
        children_dirs = tuple(
            child for child in self.children.values() if isinstance(child, Directory)
        )
        if not children_dirs:
            return (self,)
        return (self,) + tuple(
            flatten(child_dir.get_dirs_tree() for child_dir in children_dirs)
        )

    def add_children_from_ls_output(self, lines: list[str]) -> None:
        for line in lines:
            if match := LS_FILE_PATTERN.match(line):
                size, name = match.groups()
                self.children[name] = File(int(size))
            elif match := LS_DIR_PATTERN.match(line):
                name, *_ = match.groups()
                self.children[name] = Directory(parent=self)

    @classmethod
    def from_terminal_session(cls, terminal_session: tuple[Command, ...]):
        root_dir = cls()
        working_dir = root_dir
        for command, output in terminal_session:
            cmd, *args = command.split()
            match cmd, args:
                case "ls", []:
                    working_dir.add_children_from_ls_output(output)
                case "cd", [to]:
                    if to == "..":
                        working_dir = working_dir.parent or working_dir
                    else:
                        working_dir = working_dir.get_child_dir(to)
        return root_dir


def solve_part_1(terminal_session: tuple[Command, ...]) -> int:
    root_dir = Directory.from_terminal_session(terminal_session)
    return sum(
        d.size for d in root_dir.get_dirs_tree() if d.size <= DIRECTORY_SIZE_THRESHOLD
    )


def solve_part_2(terminal_session: tuple[Command, ...]) -> int:
    root_dir = Directory.from_terminal_session(terminal_session)
    unused_space = TOTAL_DISK_SPACE - root_dir.size
    space_to_free = MIN_FREE_SPACE - unused_space
    dirs_by_size_asc = sorted(root_dir.get_dirs_tree(), key=attrgetter("size"))
    return next(d.size for d in dirs_by_size_asc if d.size >= space_to_free)


if __name__ == "__main__":
    # Skip the first command that cd into root dir
    terminal_session = parse_input(sep="\n$ ", parse_fn=parse_terminal_command)[1:]
    print("Part 1:", solve_part_1(terminal_session))
    print("Part 2:", solve_part_2(terminal_session))
