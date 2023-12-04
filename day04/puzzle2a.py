# now that I've had coffee and can understand Part 2 a little better, this solution is **WAY** faster than using a queue

import collections
import datetime
from pprint import pprint

start = datetime.datetime.now()

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# read in the input
lines: list[str] = [line.rstrip() for line in open(input_filename)]

# mapping the card number to the count of winning numbers on the card
card_values: dict = {}

# Step 1: store the value of each card, so we can look it up later
for line in lines:
    card_number, numbers = line.split(':')
    discard, card_number = card_number.split()
    winners, haves = numbers.split('|')
    winning_numbers = winners.split()
    number_i_have = haves.split()

    if my_winners := set(winning_numbers).intersection(number_i_have):
        card_values[int(card_number)] = len(my_winners)
    else:
        card_values[int(card_number)] = 0

# counting how many copies there are of each card number (knowing that every card must have at least one copy)
card_counts: dict = collections.defaultdict(lambda: 1)

# Step 2: play the game by the rules, and count how many copies get played for each card number
for card_number in card_values:
    for i in range(card_values[card_number]):
        # every copy of this card creates that many copies downstream
        card_counts[card_number+i+1] += card_counts[card_number]

# using a defaultdict makes the counting easier, but makes the summing a little harder, because we have to
# explicitly ask the defaultdict for any card whose count is only 1, rather than just summing the dict's values
count = sum([card_counts[card_number] for card_number in card_values])
print(f'Found {count} total cards in {datetime.datetime.now()-start}')
