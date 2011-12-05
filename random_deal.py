import random
from game_state import *

class Randomhand:
    def __init__(self,handSize = 13):
        deck = []
        for i in range(2,15):
            deck.append(Card('C',i))
            deck.append(Card('D',i))
            deck.append(Card('H',i))
            deck.append(Card('S',i))

        sizeNHand = random.sample(deck, handSize*4)
    
        self.deal = Deal(sizeNHand[0:handSize],sizeNHand[handSize:handSize*2],sizeNHand[handSize*2:handSize*3],sizeNHand[handSize*3:handSize*4],Player.WEST)
    
