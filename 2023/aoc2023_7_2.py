import aoc
from collections import Counter
from enum import Enum, StrEnum
from functools import cached_property, total_ordering


@total_ordering
class Card(StrEnum):
    JOKER = 'J'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = 'T'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

    @cached_property
    def _card_points(self):
        return {c.value: n for n, c in enumerate(Card)}

    @property
    def points(self):
        return self._card_points[self.value]
    
    def __lt__(self, other):
        return self.points < other.points

    def __repr__(self):
        return self.value


@total_ordering
class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    FULL_HOUSE = 5
    FOUR_KIND = 6
    FIVE_KIND = 7

    @staticmethod
    def from_hand(card_list):
        card_counts = Counter(card_list)

        n_jokers = card_counts[Card.JOKER]
        card_counts[Card.JOKER] = 0
        [(top_card, _)] = card_counts.most_common(1)
        card_counts[top_card] += n_jokers

        match card_counts.most_common():
            case [(_, 5), *_] : return HandType.FIVE_KIND
            case [(_, 4), *_] : return HandType.FOUR_KIND
            case [(_, 3), (_, 2), *_] : return HandType.FULL_HOUSE
            case [(_, 3), *_] : return HandType.THREE_KIND
            case [(_, 2), (_, 2), *_] : return HandType.TWO_PAIR
            case [(_, 2), *_] : return HandType.ONE_PAIR
            case _ : return HandType.HIGH_CARD

    def __lt__(self, other):
        return self.value < other.value


@total_ordering
class Hand:
    def __init__(self, hand_str, bid_str):
        self.bid = int(bid_str)
        self.hand = [Card(c) for c in hand_str]
        self.hand_type = HandType.from_hand(self.hand)

    def __eq__(self, other):
        return self.hand == other.hand

    def __lt__(self, other):
        if self.hand_type == other.hand_type:
            return self.hand < other.hand
        return self.hand_type < other.hand_type

    def __repr__(self):
        return f"Hand: {{bid: {self.bid}, hand: {self.hand}, hand_type: {self.hand_type}}}"


def score_hands(hands):
    return sum(rank * hand.bid for (rank, hand) in enumerate(sorted(hands), start=1))


if __name__ == "__main__":
    with aoc.challenge_data(7) as data:
        hands = [Hand(*line.strip().split()) for line in data.readlines()]

    print(list(enumerate(Card)))

    for (rank, hand) in enumerate(sorted(hands), start=1):
        print(rank, hand, rank*hand.bid)

    print(score_hands(hands))