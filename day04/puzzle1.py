# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# read in the input
lines: list[str] = [line.rstrip() for line in open(input_filename)]

points_total: int = 0

# example line to parse: `Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53`
for line in lines:
    discard, numbers = line.split(':')
    winners, haves = numbers.split('|')
    winning_numbers = winners.split()  # split() with no parameters removes multiple sequential whitespaces
    number_i_have = haves.split()

    if my_winners := set(winning_numbers).intersection(number_i_have):
        points_total += 2**(len(my_winners)-1)

print(points_total)
