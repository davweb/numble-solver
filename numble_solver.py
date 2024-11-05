# -*- coding: utf-8 -*-
"""
Solve https://numble.wtf puzzles
"""

from typing import Iterable, cast
import itertools
import sys


class Step:
    """A step is a number and the calculation that produced it"""

    def __init__(self, value: int, _left=None, _op=None, _right=None) -> None:
        self.value = value
        self.left: Step | None = _left
        self.op: str | None = _op
        self.right: Step | None = _right
        self._normalize()

    def _normalize(self) -> None:
        if self.left is None or self.op is None or self.right is None:
            return

        if self.op in ('+', '×') and self.left < self.right:
            self.left, self.right = self.right, self.left

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        return self.value == other.value \
            and self.left == other.left \
            and self.op == other.op \
            and self.right == other.right

    def __hash__(self) -> int:
        return hash((self.value, self.left, self.op, self.right))

    def __lt__(self, other) -> int:
        if self.value != other.value:
            return self.value < other.value

        if len(self) != len(other):
            return len(self) < len(other)

        return self.operations() < other.operations()

    def operations(self) -> tuple[int, int, int, int]:
        """
        Return the number of each operation in the step
        """

        if self.left is None or self.op is None or self.right is None:
            return 0, 0, 0, 0

        div, mul, sub, add = [left + right for left, right in zip(self.left.operations(), self.right.operations())]

        if self.op == '+':
            add += 1
        elif self.op == '-':
            sub += 1
        elif self.op == '×':
            mul += 1
        elif self.op == '÷':
            div += 1

        return div, mul, sub, add

    def __len__(self) -> int:
        if self.left is None or self.op is None or self.right is None:
            return 1

        return len(self.left) + len(self.right)

    def __str__(self) -> str:
        """Convert to a string using as few parentheses as possible"""

        if self.left is None or self.op is None or self.right is None:
            return str(self.value)

        left_str = str(self.left)
        right_str = str(self.right)

        if self.left.op in ('+', '-') and self.op in ('×', '÷'):
            left_str = f'({left_str})'

        if (self.op == '÷' and self.right.op is not None) or (self.op in ('×', '-') and self.right.op in ('+', '-')):
            right_str = f'({right_str})'

        return f'{left_str} {self.op} {right_str}'

    def __add__(self, other):
        return Step(self.value + other.value, self, '+', other)

    def __sub__(self, other):
        return Step(self.value - other.value, self, '-', other)

    def __mul__(self, other):
        return Step(self.value * other.value, self, '×', other)

    def __truediv__(self, other):
        return Step(self.value // other.value, self, '÷', other)


def operations(numbers: list[Step]) -> Iterable[Step]:
    """
    Return the possible operations between all the Steps in a list
    """

    for left, right in itertools.combinations(numbers, 2):
        yield left + right

        # No need to multiply by 1
        if left.value != 1 and right.value != 1:
            yield left * right

    for left, right in itertools.permutations(numbers, 2):
        # Numble puzzles don't seem to use negative numbers as part of the solution and zero is no use
        if left.value > right.value:
            yield left - right

        # No need to divide by 1 and no fractions
        if right.value != 1 and left.value % right.value == 0:
            yield left / right


def solve(target: int, numbers: list[Step], results: set[Step]) -> None:
    """
    Recursively solve a Numble puzzle
    """

    for replacement in operations(numbers):
        if replacement.value == target:
            results.add(replacement)
        else:
            if replacement.left is None or replacement.right is None:
                raise ValueError('Invalid replacement')

            next_numbers = numbers + [replacement]
            next_numbers.remove(replacement.left)
            next_numbers.remove(replacement.right)
            solve(target, next_numbers, results)


def solve_puzzle(target: int, numbers: list[int]) -> Step | None:
    """
    Solve a Numble puzzle

    >>> str(solve_puzzle(375, [5, 75]))
    '75 × 5'
    >>> str(solve_puzzle(80, [5, 75]))
    '75 + 5'
    >>> str(solve_puzzle(15, [5, 75]))
    '75 ÷ 5'
    >>> str(solve_puzzle(70, [5, 75]))
    '75 - 5'
    >>> str(solve_puzzle(14, [7, 7]))
    '7 + 7'
    >>> str(solve_puzzle(28, [7, 7, 7, 7]))
    '7 + 7 + 7 + 7'
    >>> str(solve_puzzle(7, [1, 2, 7, 75]))
    '7'
    >>> str(solve_puzzle(876, {25, 100, 50, 75, 10, 3}))
    '(75 - 100 ÷ 50) × (25 - (10 + 3))'
    >>> str(solve_puzzle (591, {3, 8, 10, 25, 50, 100}))
    '(50 - 8) × (10 + 100 ÷ 25) + 3'
    """

    if target in numbers:
        return Step(target)

    results: set[Step] = set()

    solve(target, [Step(n) for n in numbers], results)

    if results:
        return cast(list[Step], sorted(results))[0]

    return None


def main() -> None:
    """
    Entry point
    """
    target = int(sys.argv[1])
    numbers = [int(n) for n in sys.argv[2:]]
    result = solve_puzzle(target, numbers)

    if result is None:
        print('No solution found.')
        sys.exit(1)
    else:
        print(f'{result} = {target}')


if __name__ == '__main__':
    main()
