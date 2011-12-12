from game_state import *
from random_deal import *
from relative_rank import *
from persistent_dictionary import PersistentDict

class SingleSuit:

    def __init__(self):
        self.rank = RelativeRank()
        self.table = PersistentDict('single_suit.dat')

    def single_suit_analysis(self,game_state):
        hands = self.rank.relative_hands(state)
        player = game_state.get_next_player()
        try:
            return self.table[(repr(hands),player)]
        except KeyError:
            value_ind = self.sure_tricks(hands,player)
            value_coop = self.sure_tricks_coop(hands,player)
            value = max(value_ind,value_coop)
            self.table[(repr(hands),player)] = value
            return value

    def sure_tricks(self,hands,player):
        """
        this assumes that it is being called on the first player in a hand
        it also does not take into account a cooperative partner
        """
        #my hand
        players_hand = hands[player]
        #everyone else's hand
        others = [x for x in Player.POSITION if x != player]
        other_hands = [hands[x] for x in others]
    
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

    def sure_tricks_coop(self,hands,player):
        """
        this assumes that it is being called on the first player in a hand
        it also does not take into account a cooperative partner
        """
        #my hand
        players_hand = hands[player]
        #my partner's hand
        partners_hand = hands[Player.NEXT[Player.NEXT[player]]]
        #my opponent's hands
        others = [x for x in Player.POSITION if x != player and x !=Player.NEXT[Player.NEXT[player]]]
        other_hands = [hands[x] for x in others]

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

    def close(self):
        self.rank.close()
        self.table.close()


if __name__ == '__main__':
    single_suit = SingleSuit()
    for i in range(1,14):
        for j in range(1,10000):
            print "%d-%d" % (i,j)
            hand = Randomhand(i).deal
            state = GameState.create_initial(hand)
            single_suit.single_suit_analysis(state)
    single_suit.close()
