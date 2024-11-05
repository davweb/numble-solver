# -*- coding: utf-8 -*-
"""
Solve https://numble.wtf puzzles
"""

from typing import Iterable
import itertools
import sys

#  A Step is number and the history of how we got there
type Step = int | tuple[int, int | tuple[Step, str, Step]]


def operations(numbers: list[Step]) -> Iterable[tuple[Step, Step, tuple[int, Step]]]:
    """
    Return the possible operations between all the Steps in a list
    """

    for left, right in itertools.combinations(numbers, 2):
        if left[0] < right[0]:
            left, right = right, left

        yield (left, right, (left[0] + right[0], (left[1], '+', right[1])))

        # No need to multiply by 1
        if left[0] != 1 and right[0] != 1:
            yield (left, right, (left[0] * right[0], (left[1], '×', right[1])))

    for left, right in itertools.permutations(numbers, 2):
        # Numble puzzles don't seem to use negative numbers as part of the solution and zero is no use
        if left[0] > right[0]:
            yield (left, right, (left[0] - right[0], (left[1], '-', right[1])))

        # No need to divide by 1 and no fractions
        if right[0] != 1 and left[0] % right[0] == 0:
            yield (left, right, (left[0] // right[0], (left[1], '÷', right[1])))


def solve(target: int, numbers: list[Step], results) -> str | None:
    """
    Recursively solve a Numble puzzle
    """

    for left, right, replacement in operations(numbers):
        if replacement[0] == target:
            results.add(replacement[1])

        next_numbers = [n for n in numbers if n not in (left, right)] + [replacement]
        solve(target, next_numbers, results)


def solve_puzzle(target: int, numbers: list[int]) -> str | None:
    """
    Solve a Numble puzzle

    >>> solve_puzzle(375, [5, 75])
    '75 × 5'
    >>> solve_puzzle(80, [5, 75])
    '75 + 5'
    >>> solve_puzzle(15, [5, 75])
    '75 ÷ 5'
    >>> solve_puzzle(70, [5, 75])
    '75 - 5'
    >>> solve_puzzle(14, [7, 7])
    '7 + 7'
    >>> solve_puzzle(7, [1, 2, 7, 75])
    '7'
    >>> solve_puzzle(876, {25, 100, 50, 75, 10, 3})
    '(75 - 100 ÷ 50) × (25 - (10 + 3))'
    >>> solve_puzzle (591, {3, 8, 10, 25, 50, 100})
    '(50 - 8) × (10 + 100 ÷ 25) + 3'
    """

    if target in numbers:
        return str(target)

    results = set()
    solve(target, [(n, n) for n in numbers], results)

    def sort_key(expression):
        return expression_length(expression), expression_depth(expression), format_expression(expression)

    if results:
        return format_expression(sorted(results, key=sort_key)[0])

    return None


def format_expression(expression):
    """Convert an expression in nested tuples to a string, using as few brackets as possible"""

    if isinstance(expression, int):
        return str(expression)

    left, op, right = expression
    left_op = None if isinstance(left, int) else left[1]
    right_op = None if isinstance(right, int) else right[1]

    left_str = format_expression(left)
    right_str = format_expression(right)

    if left_op in ('+', '-') and op in ('×', '÷'):
        left_str = f'({left_str})'

    if (op == '÷' and right_op is not None) or (op in ('×', '-') and right_op in  ('+', '-')):
        right_str = f'({right_str})'

    return f'{left_str} {op} {right_str}'


def expression_length(expression):
    """Count the number of elements an expression"""
    if isinstance(expression, int):
        return 1

    return expression_length(expression[0]) + expression_length(expression[2])


def expression_depth(expression):
    """Calculate the nesting of an expression"""
    if isinstance(expression, int):
        return 0

    left_depth = 1 + expression_depth(expression[0])
    right_depth = 1 + expression_depth(expression[2])
    return max(left_depth, right_depth)


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
