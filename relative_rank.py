from persistent_dictionary import PersistentDict
from game_state import *

class RelativeRank:
    def __init__(self,config):
        self.table = PersistentDict(config.get('Search','relative_rank'),mode=0666)

    def relative_hands(self,game_state):
        hands = {}
        for player,hand in game_state.hands.iteritems():
            hands[player] = [self.relative_rank(game_state,card) for card in hand]
        return hands

    def relative_rank(self,game_state, card):
        state_of_suit = game_state.get_state_of_suit(card.suit)
        return Card(card.suit,self.get_relative_rank(state_of_suit,card.value))

    def get_relative_rank(self,state,card):
        return self.table[(state<<4)+(card-2)]

    def fillTable(self):
        for i in range(1,8192):
            for j in range(0,13):
                if i & (1<<j):
                    rank = 0
                    for x in range(0,j):
                        if i & (1<<x):
                            rank += 1
                    self.table[(i<<4)+j] = rank

    def close(self):
        self.table.close()

if __name__ == '__main__':
    ranks = RelativeRank()
    ranks.fillTable()
    ranks.close() 
