from puzzle2 import Hand, HandType

test_cases = [
    # testing five of a kind with jokers
    ('AAAAA', HandType.FIVE_OF_A_KIND),
    ('AAAAJ', HandType.FIVE_OF_A_KIND),
    ('AAAJJ', HandType.FIVE_OF_A_KIND),
    ('AAJJJ', HandType.FIVE_OF_A_KIND),
    ('AJJJJ', HandType.FIVE_OF_A_KIND),
    ('JJJJJ', HandType.FIVE_OF_A_KIND),

    # testing four of a kind with jokers
    ('TAAAA', HandType.FOUR_OF_A_KIND),
    ('TAAAJ', HandType.FOUR_OF_A_KIND),
    ('TAAJJ', HandType.FOUR_OF_A_KIND),
    ('TTAJJ', HandType.FOUR_OF_A_KIND),
    ('TAJJJ', HandType.FOUR_OF_A_KIND),

    # testing full house with jokers
    ('TTAAA', HandType.FULL_HOUSE),
    ('TTAAJ', HandType.FULL_HOUSE),
    ('TTAJJ', HandType.FOUR_OF_A_KIND),

    # testing three of a kind with jokers
    ('T2AAA', HandType.THREE_OF_A_KIND),
    ('T2AAJ', HandType.THREE_OF_A_KIND),
    ('T2AJJ', HandType.THREE_OF_A_KIND),

    # testing two pair with jokers
    ('22AAT', HandType.TWO_PAIR),

    # testing one pair with jokers
    ('22345', HandType.ONE_PAIR),
    ('2J345', HandType.ONE_PAIR),

    # testing high card with jokers
    ('23456', HandType.HIGH_CARD),
]

print(f'Executing {len(test_cases)} tests...')

for cards, hand_type in test_cases:
    h = Hand(cards, 0)
    if h.type != hand_type:
        print(f'test failed: {cards}  expected {hand_type} got {h.type}')

print('Done.')
