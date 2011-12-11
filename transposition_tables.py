import shelve
from game_state import *

class TranspositionTable:
  """
  This class is a basic map from a GameState
  to the (current) max number of tricks that
  can be taken by the current player's team.
  
  We only update the cache when we see a new
  value which is larger than the old value

  python has a data structure shelve,
  which is essentially a persistent dictionary.
  Thus, we pass a filename to the initializer
  and save all key-values to that file.
  Therefore, as we run more and more searches,
  we get a better and better cache.

  shelve requires that all keys be strings,
  so we simply use repr(game_state)
  """
  def __init__(self,file):
    self.table = shelve.open(file)
  

  def checkCache(self,game_state):
    if repr(game_state) in self.table:
        return self.table[repr(game_state)]
    else:
        return -1

  def saveToCache(self,game_state,newTricks):
      if repr(game_state) in self.table:
          oldTricks = self.table[repr(game_state)]
          if newTricks > oldTricks:
              self.table[repr(game_state)] = newTricks
      else:
          self.table[repr(game_state)] = newTricks

  def close(self):
      self.table.close()
      
  
