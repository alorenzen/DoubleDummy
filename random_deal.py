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

        hands = dict(zip(Player.POSITION,
                         [sorted(sizeNHand[0         :handSize  ],reverse=True),
                          sorted(sizeNHand[handSize  :handSize*2],reverse=True),
                          sorted(sizeNHand[handSize*2:handSize*3],reverse=True),
                          sorted(sizeNHand[handSize*3:handSize*4],reverse=True)]))
        self.deal = Deal(hands,Player.WEST)
    
class Montehand: 
    def __init__(self,handSize = 13, numtrials = 2):
        deck = []
        for i in range(2,15):
            deck.append(Card('C',i))
            deck.append(Card('D',i))
            deck.append(Card('H',i))
            deck.append(Card('S',i))
            
        sizeNHand = random.sample(deck, handSize*4)
        
        player_hand = sizeNHand[0, handSize]                         
        partner_hand = sizeNHand[handSize, handSize*2]
        other_hands = sizeNHand[handSize*2, handSize*4]
        self.dealList = []
        makeOtherHands(numtrials)

        def makeOtherHands(numTrials):
            for i in range(0,numTrials):
                other_hands = random.shuffle(other_hands)
                other_player_one = other_hands[0, handSize]
                other_player_two = other_hands[handSize, handSize*2]
           
                monteHands = dict(zip(Player.POSITION,
                                      [sorted(player_hand,reverse=True),
                                       sorted(other_player_one,reverse=True),
                                       sorted(partner_hand,reverse=True),
                                       sorted(other_player_two,reverse=True)]))
                
                self.dealList = dealList.append(Deal(monteHands,Player.WEST))
