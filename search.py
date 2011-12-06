from game_state import *
from random_deal import Randomhand

def ddsearch(game_state, goal):
    """
    given a game_state, determine whether
    or not it is possible for north/south to 
    take goal number of tricks
    """
    #print goal
    if game_state.tricks_left() == 0:
        return game_state.team_win_last_trick(Player.TEAM[game_state.get_next_player()])
    if goal <= 0:
        return True
    if goal > game_state.tricks_left():
        return False
    
    player = game_state.get_next_player()
    actions = game_state.get_actions_for_player(player)
    #print player
    for action in actions:
        #print action
        next_state = game_state.play_card(action)
        if game_state.state_switch_teams(next_state):
            next_goal = game_state.tricks_left() - goal + 1
            if next_state.is_new_trick():
                next_goal = next_goal - 1
            result = not ddsearch(next_state,next_goal)
        else: 
            if next_state.is_new_trick():
                next_goal = goal - 1
            else:
                next_goal = goal
            result = ddsearch(next_state,next_goal)
        #print result
        if result:
            return True

    return False

def search(state):
    low=0
    high=state.tricks_left()+1
    while low+1<high:
        goal = (low+high)/2
        print goal
        if ddsearch(state,goal):
            low = goal
        else:
            high = goal
    return low

if __name__ == '__main__':
    hands = {}
    hands[Player.NORTH] = [Card(Suit.CLUBS ,3),Card(Suit.HEARTS,3)]
    hands[Player.SOUTH] = [Card(Suit.HEARTS,2),Card(Suit.HEARTS,4)]
    hands[Player.EAST]  = [Card(Suit.CLUBS ,2),Card(Suit.SPADES,4)]
    hands[Player.WEST]  = [Card(Suit.SPADES,3),Card(Suit.SPADES,5)]
    start = Deal(hands,Player.WEST)
    state = GameState.create_initial(start)
    #state = GameState.create_initial(Randomhand(7).deal)
    print search(state)

        
