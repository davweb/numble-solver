# -*- coding: utf-8 -*-
"""
Solve https://numble.wtf puzzles
"""

import sys

OPERATIONS = ['+', '×', '-', '÷']


def solve(target: int, numbers: set[int]) -> list[str] | None:
    """
    Recursively solve a Numble puzzle

    >>> solve(375, {5, 75})
    ['5 × 75 = 375']
    >>> solve(80, {5, 75})
    ['5 + 75 = 80']
    >>> solve(15, {5, 75})
    ['75 ÷ 5 = 15']
    >>> solve(70, {5, 75})
    ['75 - 5 = 70']
    >>> solve(876, {25, 100, 50, 75, 10, 3})
    ['100 × 75 = 7500', '7500 + 50 = 7550', '7550 ÷ 25 = 302', '302 - 10 = 292', '292 × 3 = 876']
    """

    for number in numbers:
        if number == target:
            return []

        next_numbers = numbers - {number}

        for operation in OPERATIONS:

            match operation:
                case '+':
                    if number > target:
                        continue
                    next_target = target - number
                case '-':
                    next_target = target + number
                case '×':
                    if number == 1 or target % number != 0:
                        continue
                    next_target = target // number
                case '÷':
                    if number == 1:
                        continue
                    next_target = target * number

            result = solve(next_target, next_numbers)

            if result is not None:
                result.append(f'{next_target} {operation} {number} = {target}')
                return result

    return None


def main() -> None:
    """
    Entry point
    """
    numbers = [int(n) for n in sys.argv[1:]]
    result = solve(numbers[0], set(numbers[1:]))

    if result is None:
        print('No solution found.')
        sys.exit(1)
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    main()
