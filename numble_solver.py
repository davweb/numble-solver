# -*- coding: utf-8 -*-
"""
Solve https://numble.wtf puzzles
"""

from typing import Iterable
import itertools
import sys

#  A Step is number and the history of how we got there
type Step = tuple[int, str]


def operations(numbers: list[Step]) -> Iterable[tuple[Step, Step, Step]]:
    """
    Return the possible operations between all the Steps in a list
    """

    for left, right in itertools.combinations(numbers, 2):
        yield (left, right, (left[0] + right[0], f'({left[1]} + {right[1]})'))

        # No need to multiply by 1
        if left[0] != 1 and right[0] != 1:
            yield (left, right, (left[0] * right[0], f'({left[1]} × {right[1]})'))

    for left, right in itertools.permutations(numbers, 2):
        # Numble puzzles don't seem to use negative numbers as part of the solution and zero is no use
        if left[0] > right[0]:
            yield (left, right, (left[0] - right[0], f'({left[1]} - {right[1]})'))

        # No need to divide by 1 and no fractions
        if right[0] != 1 and left[0] % right[0] == 0:
            yield (left, right, (left[0] // right[0], f'({left[1]} ÷ {right[1]})'))


def solve(target: int, numbers: list[Step]) -> str | None:
    """
    Recursively solve a Numble puzzle
    """

    for left, right, replacement in operations(numbers):
        if replacement[0] == target:
            # Strip the outer parentheses
            return replacement[1][1:-1]

        next_numbers = [n for n in numbers if n != left and n != right] + [replacement]
        result = solve(target, next_numbers)

        if result is not None:
            return result

    return None


def solve_puzzle(target: int, numbers: list[int]) -> str | None:
    """
    Solve a Numble puzzle

    >>> solve_puzzle(375, [5, 75])
    '5 × 75'
    >>> solve_puzzle(80, [5, 75])
    '5 + 75'
    >>> solve_puzzle(15, [5, 75])
    '75 ÷ 5'
    >>> solve_puzzle(70, [5, 75])
    '75 - 5'
    >>> solve_puzzle(14, [7, 7])
    '7 + 7'
    >>> solve_puzzle(7, [1, 2, 7, 75])
    '7'
    >>> solve_puzzle(876, {25, 100, 50, 75, 10, 3})
    '(25 - (3 + 10)) × (75 - (100 ÷ 50))'
    >>> solve_puzzle (591, {3, 8, 10, 25, 50, 100})
    '3 + ((50 - 8) × (10 + (100 ÷ 25)))'
    """

    if target in numbers:
        return str(target)

    return solve(target, [(n, str(n)) for n in numbers])


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
