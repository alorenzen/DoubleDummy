from game_state import *
from random_deal import *

def sure_tricks(game_state):
    """
    this assumes that it is being called on the first player in a hand
    it also does not take into account a cooperative partner
    """
    #my hand
    player = game_state.get_next_player()
    players_hand = game_state.get_actions_for_player(player)
    #everyone else's hand
    others = [x for x in Player.POSITION if x != player]
    other_hands = [game_state.get_actions_for_player(x) for x in others]
    
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

def sure_tricks_coop(game_state):
    """
    this assumes that it is being called on the first player in a hand
    it also does not take into account a cooperative partner
    """
    player = game_state.get_next_player()
    #my hand
    players_hand = game_state.get_actions_for_player(player)
    #my partner's hand
    partners_hand = game_state.get_actions_for_player(Player.NEXT[Player.NEXT[player]])
    #my opponent's hands
    others = [x for x in Player.POSITION if x != player and x !=Player.NEXT[Player.NEXT[player]]]
    other_hands = [game_state.get_actions_for_player(x) for x in others]


    def reduce_suit(suit):
        value = lambda x:x.value
        def max_suit(hand):
            try:
                return max(filter(lambda x:x.suit == suit,hand),key=value)
            except ValueError:
                return Card(suit=suit,value=0)

        #gives me the cards in the player's suit
        player_suit = [x for x in players_hand if x.suit == suit]
        #gives me the cards in the partner's suit
        partner_suit = [x for x in partners_hand if x.suit == suit]
        #count my partner's cards, my cards
        playerNumCards = len(player_suit)
        partnerNumCards = len(partner_suit)
        
        #this is the theoretical max of sure tricks in this suit
        upperBound = min(partnerNumCards, playerNumCards)
          
        #gets the max card of all other players in the desired suit
        other_max = map(lambda y: max_suit(y),other_hands)
           
        #counts the number of declarer/partner cards which are larger than all opponent's max
        numBetterCards = len(filter(lambda x: x == max(other_max + [x], key=value), player_suit))+len(filter(lambda x: x == max(other_max + [x], key=value), partner_suit))

        return min(numBetterCards, upperBound)

    return reduce(lambda x,y: x+reduce_suit(y), Suit.SUITS, 0)


        
if __name__ == '__main__':
    hand = Randomhand().deal
    state = GameState.create_initial(hand)
    print state
    print sure_tricks(state)
