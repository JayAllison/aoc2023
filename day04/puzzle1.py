from pprint import pprint

input_filename: str = 'sample_data'
# input_filename: str = 'input.txt'

# read in the input
lines: list[str] = [line.rstrip() for line in open(input_filename)]

points_total = 0

for line in lines:
    discard, numbers = line.split(':')
    winners, haves = numbers.split('|')
    winning_numbers = winners.split()
    number_i_have = haves.split()

    my_winners = set(winning_numbers).intersection(number_i_have)
    if my_winners:
        points_total += 2**(len(my_winners)-1)

print(points_total)
