# import pprint
import datetime
from typing import Iterable

# input_filename: str = 'sample_data0'
# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def is_match(potential_spring_record: str, given_counts: list[int]) -> bool:
    # find each group of '#' chars and count the length of them - split() on spaces removes multiples
    measured_counts = [len(group) for group in potential_spring_record.replace('.', ' ').split()]

    # does that measured count sequence match the count sequence we were given?
    return measured_counts == given_counts


# there has got to be a ready-made wy to do this, but I didn't immediately find it - later I realized it was as easy as:
#   itertools.product('.#', repeat=count)
# I am not worried about recursion depth - I think the max is 20 or so (for Part 1, it was actually 18)
# use a generator to avoid memory bloat
def permutate(count: int) -> Iterable[str]:
    # recursively generate permutations of '.' and '#' at every position for <count> positions
    if count == 0:
        return None
    elif count == 1:
        yield '.'
        yield '#'
    else:
        for p in permutate(count - 1):
            yield p + '.'
            yield p + '#'


# use a generator to avoid memory bloat
def generate_possibilities(spring_record: str) -> Iterable[str]:
    # given a record, generate every combination of replacing '?' with either '.' or '#'
    q_count: int = spring_record.count('?')
    if q_count == 0:
        return [spring_record]

    for replacement in permutate(q_count):
        possibility: str = spring_record
        for replacement_char in replacement:
            possibility = possibility.replace('?', replacement_char, 1)
        yield possibility


def solve(filename: str) -> int:
    half_lines: list[list[str]] = [line.rstrip().split() for line in open(filename).readlines()]
    records: list[tuple[str, list[int]]] = [(half[0], [int(i) for i in half[1].split(',')]) for half in half_lines]

    total: int = 0
    # max_qs: int = 0

    # for every entry we were given, check the possibilities against the actual to see how many matches we find
    for spring_record, spring_counts in records:
        sub_total: int = 0
        # q_count: int = spring_record.count('?')
        # max_qs = max(max_qs, q_count)
        # print(f'{spring_record} ({q_count} ?\'s): {spring_counts} -> ', end='', flush=True)
        for possibility in generate_possibilities(spring_record):
            # print(f'checking {possibility} against {spring_counts}')
            if is_match(possibility, spring_counts):
                # print(' -> match!')
                sub_total += 1
        # print(sub_total)
        total += sub_total

    # print(f'Max ? count = {max_qs}')
    return total


if __name__ == '__main__':
    before = datetime.datetime.now()
    print(f'Found {solve(input_filename)} possible arrangements in {datetime.datetime.now() - before}')
