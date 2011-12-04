"""
Classes to represent Game State.
@author t. andrew lorenzen, e.d. Outterson
"""
from collections import namedtuple

class CardNotPlayable(Exception):
    """
    Raised when a card which is not allowed is actually played in a trick.
    """
    pass

class Card(namedtuple('Card','suit value')):
    """
    A Single Card, which has a suit and a value
    """
    __slots__ = ()
    """
    helps keep memory requirements low 
    by preventing the creation of instance dictionaries
    """

    def __str__(self):
        return self.suit + str(self.value)
    def __repr__(self):
        return self.__str__()


class Suit:
    CLUBS    = 'C'
    DIAMONDS = 'D'
    HEARTS   = 'H'
    SPADES   = 'S'
    NONE     = 'N'

class Player:
    NORTH = 'North'
    SOUTH = 'South'
    EAST  = 'East'
    WEST  = 'West'

    NEXT = {NORTH:EAST,
            EAST:SOUTH,
            SOUTH:WEST,
            WEST:NORTH}

class Trick:
    def __init__(self):
        self.cards = {}
        self.suit = Suit.NONE

    def play_card(self,card,player):
        self.cards[card] = player
        if self.suit == Suit.NONE:
            self.suit = card.suit

    def finished(self):
        return len(self.cards) == 4

    def winner(self):
        winning_card = max([x for x in self.cards.keys() if x.suit == self.suit],
                           key=lambda x: x.value)
        return self.cards[winning_card]
                              


class GameState:
    def __init__(self, prevState = None):
        if prevState != None:
            self.hands = prevState.hands.copy()
            self.next_player = prevState.next_player
            self.current_trick = prevState.current_trick
            self.tricks = prevState.tricks
        else:
            self.hands = {}
            self.next_player = Player.WEST
            self.current_trick = Trick()
            self.tricks = []

    @classmethod
    def create_initial(cls,starting_deal):
        g = GameState()
        g.hands[Player.NORTH] = starting_deal.north_cards
        g.hands[Player.SOUTH] = starting_deal.south_cards
        g.hands[Player.EAST] = starting_deal.east_cards
        g.hands[Player.WEST] = starting_deal.west_cards
        g.next_player = starting_deal.starting_player
        return g
    
    def get_next_player(self):
        return self.next_player

    def get_actions(self):
        return self.get_actions_for_player(self.next_player)

    def get_actions_for_player(self,player):
        return self.get_playable_cards(self.hands[player],self.current_trick)
    
    def get_playable_cards(self,hand,trick):
        if trick.suit == Suit.NONE:
            return hand
        else:
            followSuit = [x for x in hand if x.suit == trick.suit]
            if len(followSuit) == 0:
                return hand
            return followSuit

    def play_card(self,card):
        if card not in self.get_actions():
            raise CardNotPlayable()
        current_hand = self.hands[self.next_player]
        nextState = GameState(self)
        nextState.hands[self.next_player] = [x for x in current_hand if x != card]
        nextState.current_trick.play_card(card,self.next_player)
        if nextState.current_trick.finished():
            nextState.tricks.append(nextState.current_trick)
            nextState.next_player = nextState.current_trick.winner()
            nextState.current_trick = Trick()
        else:
            nextState.next_player = Player.NEXT[self.next_player]
        return nextState

    def get_NS_trick_count(self):
        return len([x for x in tricks if x.winner == NORTH or x.winner == SOUTH])


class Deal:
    def __init__(self, north_cards, east_cards, south_cards, west_cards, starting_player = Player.WEST):
        self.north_cards = north_cards
        self.east_cards = east_cards
        self.south_cards = south_cards
        self.west_cards = west_cards
        self.starting_player = starting_player


if __name__ == '__main__':
    north_cards = [Card(Suit.CLUBS,3),Card(Suit.HEARTS,3)]
    south_cards = [Card(Suit.HEARTS,2),Card(Suit.HEARTS,4)]
    east_cards = [Card(Suit.CLUBS,2),Card(Suit.SPADES,4)]
    west_cards = [Card(Suit.SPADES,3),Card(Suit.SPADES,5)]
    start = Deal(north_cards,east_cards,south_cards,west_cards,Player.WEST)
    state = GameState.create_initial(start)
    for x in range(0,4):
        print state.get_next_player()
        actions = state.get_actions()
        print actions
        state = state.play_card(actions[0])
    print map(lambda x: x.suit + str(x.cards),state.tricks)
    print state.get_next_player()

    


