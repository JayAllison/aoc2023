import collections
import datetime
from pprint import pprint

start = datetime.datetime.now()

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# read in the input
lines: list[str] = [line.rstrip() for line in open(input_filename)]

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

# Step 2: play the game by the rules, and count how many cards get played
# using a deque so we can efficiently pop from the front - every time a copy is "won", add it to the queue to play again
cards_to_play = collections.deque(card_values.keys())
count = 0
while cards_to_play:
    count += 1
    card_number = cards_to_play.popleft()
    for i in range(card_values[card_number]):
        cards_to_play.append(card_number + i + 1)

print(f'Found {count} total cards in {datetime.datetime.now()-start}')
