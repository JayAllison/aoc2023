from enum import Enum

# input_filename = 'sample_data'
# input_filename = 'test_cards'
input_filename = 'input.txt'

CARD_STRENGTHS = 'J23456789TQKA'

debug = False
# debug = True


def dprint(s):
    global debug
    if debug:
        print(s)


class HandType(Enum):
    UNKNOWN = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand:

    cards: str = None
    bid: int = 0
    type: HandType = HandType.UNKNOWN

    def __init__(self, hand_of_cards: str, hand_bid: int):
        self.cards = hand_of_cards
        self.bid = hand_bid
        self.evaluate()

    def __gt__(self, other):
        if self.type != other.type:
            return self.type.value > other.type.value

        for i in range(len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return CARD_STRENGTHS.find(self.cards[i]) > CARD_STRENGTHS.find(other.cards[i])

        print(f'error! gt comparison failed to determine result for {self.cards} and {other.cards}')
        return False

    def __eq__(self, other):
        return self.type == other.type and self.cards == other.cards

    def __lt__(self, other):
        return not self > other and not self == other

    def evaluate(self):
        card_counts = [self.cards.count(c) for c in CARD_STRENGTHS if c != 'J']
        j_counts = self.cards.count('J')
        dprint(f'{self.cards} {card_counts} {j_counts}')

        if max(card_counts) + j_counts == 5:
            self.type = HandType.FIVE_OF_A_KIND
        elif max(card_counts) + j_counts == 5:
            self.type = HandType.FIVE_OF_A_KIND
        elif max(card_counts) + j_counts == 4:
            self.type = HandType.FOUR_OF_A_KIND
        elif 3 in card_counts and 2 in card_counts:  # J does not help here
            self.type = HandType.FULL_HOUSE
        elif 2 in card_counts and card_counts.count(2) == 2 and j_counts == 1:
            self.type = HandType.FULL_HOUSE
        elif max(card_counts) + j_counts == 3:
            self.type = HandType.THREE_OF_A_KIND
        elif 2 in card_counts and card_counts.count(2) == 2 and j_counts == 0:
            self.type = HandType.TWO_PAIR
        elif max(card_counts) + j_counts == 2:
            self.type = HandType.ONE_PAIR
        elif card_counts.count(1) == 5:  # no J's will be here
            self.type = HandType.HIGH_CARD
        else:
            print(f'cannot determine card type for {self.cards} with counts {card_counts}')


def solve():
    hands = []

    for line in open(input_filename):
        the_cards, the_bid = line.rstrip().split()
        hands.append(Hand(the_cards, int(the_bid)))

    rank = 1
    winnings = 0
    for hand in sorted(hands):
        # print(f'{rank} {hand.cards}: {hand.type} {hand.bid}')
        winnings += rank * hand.bid
        rank += 1

    print(f'Total winnings: {winnings}')


if __name__ == '__main__':
    solve()
