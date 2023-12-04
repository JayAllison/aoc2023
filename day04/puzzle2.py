import collections
from pprint import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# read in the input
lines: list[str] = [line.rstrip() for line in open(input_filename)]

cards = {}

for line in lines:
    card, numbers = line.split(':')
    discard, card_id = card.split()
    winners, haves = numbers.split('|')
    winning_numbers = winners.split()
    number_i_have = haves.split()

    my_winners = set(winning_numbers).intersection(number_i_have)
    if my_winners:
        cards[int(card_id)] = len(my_winners)
    else:
        cards[int(card_id)] = 0

cards_to_play = collections.deque(cards.keys())
count = 0
while cards_to_play:
    card = cards_to_play.popleft()
    count += 1
    for i in range(cards[card]):
        cards_to_play.append(card + i + 1)

print(count)
