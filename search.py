import os
import sys
from game_state import *
from random_deal import Randomhand
from single_suit import *
from transposition_tables import TranspositionTable

def ddsearch(game_state,goal,transTable):
    """
    given a game_state, determine whether
    or not it is possible for current_player's 
    team to take goal number of tricks
    """
    player = game_state.get_next_player()
    if transTable.checkCache(game_state) >= goal:
        return True
    if game_state.tricks_left() == 1:
        if game_state.team_win_last_trick(Player.TEAM[player]):
            transTable.saveToCache(game_state,1)
            return True
        else:
            return False
    if goal <= 0:
        return True
    if goal > game_state.tricks_left():
        return False
    if game_state.is_new_trick():
        tricks = sure_tricks(game_state)
        if tricks >= goal:
            transTable.saveToCache(game_state,goal)
            return True
    
    actions = game_state.get_actions_for_player(player)
    for action in actions:
        next_state = game_state.play_card(action)
        if game_state.state_switch_teams(next_state):
            next_goal = game_state.tricks_left() - goal + 1
            if next_state.is_new_trick():
                next_goal = next_goal - 1
            result = not ddsearch(next_state,next_goal,transTable)
        else: 
            if next_state.is_new_trick():
                next_goal = goal - 1
            else:
                next_goal = goal
            result = ddsearch(next_state,next_goal,transTable)
        if result:
            transTable.saveToCache(game_state,goal)
            return True
    return False

def search(state,transTable):
    low=0
    high=state.tricks_left()+1
    while low+1<high:
        goal = (low+high)/2
        print goal
        if ddsearch(state,goal,transTable):
            low = goal
        else:
            high = goal
    return low

if __name__ == '__main__':
    try:
        transpo_file = 'transposition_table.dat'
        transTable = TranspositionTable(transpo_file)
        C = Suit.CLUBS
        D = Suit.DIAMONDS
        H = Suit.HEARTS
        S = Suit.SPADES
        
        hands = {}
        hands[Player.NORTH] = [Card(S,14),Card(S,13),Card(S,12),Card(H,9 ),Card(D,8),Card(C,2)]
        hands[Player.EAST]  = [Card(S,9 ),Card(S,6 ),Card(S,5 ),Card(H,6 ),Card(D,9),Card(C,5)]
        hands[Player.SOUTH] = [Card(S,3 ),Card(H,7 ),Card(H,3 ),Card(D,11),Card(D,2),Card(C,3)]
        hands[Player.WEST]  = [Card(S,11),Card(S,10),Card(S,8 ),Card(H,5 ),Card(H,4),Card(H,2)]
        start = Deal(hands,Player.NORTH)
        if(len(sys.argv) > 1):
            state = GameState.create_initial(Randomhand(int(sys.argv[1])).deal)
        else:
            state = GameState.create_initial(start)
        print state.hands
        print search(state,transTable)
    finally:
        transTable.close()
