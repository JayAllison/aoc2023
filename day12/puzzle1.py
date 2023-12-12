import pprint
import datetime

# input_filename: str = 'sample_data0'
# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def is_match(spring_record: str, spring_counts: list[int]) -> bool:
    # find each group of '#' chars and count the length of them - split() on spaces removes multiples
    broken_counts = [len(group) for group in spring_record.replace('.', ' ').split()]

    # does that measured count sequence match the count sequence we were given?
    return broken_counts == spring_counts


# there has got to be a ready-made wy to do this, but I didn't immediately find it - will look harder later
# I am not worried about recursion depth - I think the max is 20 or so
def permutate(count: int) -> list[str]:
    if count == 0:
        return []
    elif count == 1:
        return ['.', '#']

    results = []
    for p in permutate(count - 1):
        results.append('.' + p)
        results.append('#' + p)

    return results


# given a record, generate every combination of replacing '?' with either '.' or '#'
def generate_possibilities(spring_record: str) -> list[str]:
    q_count = spring_record.count('?')
    if q_count == 0:
        return [spring_record]

    replacements = permutate(q_count)

    possibilities = []
    for replacement in replacements:
        possibility = spring_record
        for replacement_char in replacement:
            possibility = possibility.replace('?', replacement_char, 1)
        possibilities.append(possibility)

    return possibilities


def solve(filename: str) -> int:
    lines = [line.rstrip() for line in open(filename).readlines()]
    half_lines = [line.split() for line in lines]
    records = [[half[0], [int(i) for i in half[1].split(',')]] for half in half_lines]

    total = 0
    for spring_record, spring_counts in records:
        sub_total = 0
        # print(f'{spring_record} : {spring_counts} -> ', end='', flush=True)
        possibilities = generate_possibilities(spring_record)
        for possibility in possibilities:
            # print(f'checking {possibility} against {spring_counts}')
            if is_match(possibility, spring_counts):
                # print(' -> match!')
                sub_total += 1
        # print(sub_total)
        total += sub_total

    return total


if __name__ == '__main__':
    before = datetime.datetime.now()
    print(f'Found {solve(input_filename)} possible arrangements in {datetime.datetime.now() - before}')
