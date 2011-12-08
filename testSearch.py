from pbn_parser import *
from game_state import *
from search import *

if __name__ == '__main__':
    pbnstr = file('pbn_files/OptimumResultTable.pbn').read()
    expected = importPBN(pbnstr)
    for player in Player.POSITION:
        (state,tricks) = expected[player]
        actual = search(GameState.create_initial(state))
        if actual != value:
            raise "Actual(%d) does not match expected(%d)" % (actual,value)
