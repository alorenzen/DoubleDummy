from game_state import *
from random_deal import *

def sure_tricks(game_state):
    """
    this assumes that it is being called on the first player in a hand
    it also does not take into account a cooperative partner
    """
    player = game_state.get_next_player()
    players_hand = game_state.get_actions_for_player(player)
    others = [x for x in Player.POSITION if x != player]
    other_hands = [game_state.get_actions_for_player(x) for x in others]
    #print other_hands

    def reduce_suit(suit):
        value = lambda x:x.value
        def max_suit(hand):
            try:
                return max(filter(lambda x:x.suit == suit,hand),key=value)
            except ValueError:
                return Card(suit=suit,value=0)

        player_suit = [x for x in players_hand if x.suit == suit]
        #gets a list of the max card for each other player that is in the desired suit
        other_max = map(lambda y: max_suit(y),other_hands)
        #counts the number of declarer cards which are larger than all other players max card
        return len(filter(lambda x: x == max(other_max + [x], key=value), player_suit))

    return reduce(lambda x,y: x+reduce_suit(y), Suit.SUITS, 0)
        
if __name__ == '__main__':
    hand = Randomhand().deal
    state = GameState.create_initial(hand)
    print state
    print sure_tricks(state)
