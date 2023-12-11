from collections import Counter
from enum import Enum, StrEnum
from functools import cached_property, total_ordering


@total_ordering
class Card(StrEnum):
    TWO = '2'
    THREE = '3'
    FOUR = '4' 
    FIVE = '5' 
    SIX = '6' 
    SEVEN = '7' 
    EIGHT = '8' 
    NINE = '9'
    TEN = 'T'
    JACK = 'J' 
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
        match [n for _, n in Counter(card_list).most_common()]:
            case [5, *_] : return HandType.FIVE_KIND
            case [4, *_] : return HandType.FOUR_KIND
            case [3, 2, *_] : return HandType.FULL_HOUSE
            case [3, *_] : return HandType.THREE_KIND
            case [2, 2, *_] : return HandType.TWO_PAIR
            case [2, *_] : return HandType.ONE_PAIR
            case [1, *_] : return HandType.HIGH_CARD
        raise ValueError(card_list)

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


def solution(data, debug=False):
    return score_hands(
        [Hand(*line.strip().split()) for line in data.readlines()]
    )