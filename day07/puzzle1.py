from enum import Enum

# input_filename = 'sample_data'
input_filename: str = 'input.txt'

CARD_STRENGTHS: str = '23456789TJQKA'


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
        self._evaluate_hand_type()

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

    def _evaluate_hand_type(self):
        # if there are only 5 cards in the hand, then counting how many of each strength card we have is all we need
        card_counts: list[int] = [self.cards.count(c) for c in CARD_STRENGTHS]
        if 5 in card_counts:  # if there is 5 of anything, then there is 0 of anything else - must be Five of a Kind
            self.type = HandType.FIVE_OF_A_KIND
        elif 4 in card_counts:  # if there is 4 of anything, then there is only 1 of anything else - so, Four of a Kind
            self.type = HandType.FOUR_OF_A_KIND
        elif 3 in card_counts and 2 in card_counts:  # is there is 3 of anything, the other two could be a pair or not
            self.type = HandType.FULL_HOUSE  # if the other two are a pair, it's a Full House
        elif 3 in card_counts:  # if the other two are not a pair, then it's just Three of a Kind
            self.type = HandType.THREE_OF_A_KIND
        elif 2 in card_counts and card_counts.count(2) == 2:  # if there is more than one pair, it must be Two Pair
            self.type = HandType.TWO_PAIR
        elif 2 in card_counts:  # if we've gotten here then there is not two pairs, so it must be One Pair
            self.type = HandType.ONE_PAIR
        elif card_counts.count(1) == 5: # otherwise, if all of the cards are different, then it is High Card
            self.type = HandType.HIGH_CARD
        else:
            print(f'cannot determine card type for {self.cards} with counts {card_counts}')


# Step 1: read in the input file
cards_and_bids: list[(str, str)] = [line.rstrip().split() for line in open(input_filename)]

# Step 2: parse the input
hands: list[Hand] = [Hand(cards_and_bid[0], int(cards_and_bid[1])) for cards_and_bid in cards_and_bids]

# Step 3: solve the puzzle
rank: int = 1
winnings: int = 0
for hand in sorted(hands):
    # print(f'{rank} {hand.cards}: {hand.type} {hand.bid}')
    winnings += rank * hand.bid
    rank += 1

print(f'Total winnings: {winnings}')
