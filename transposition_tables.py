import shelve
import gdbm
from configuration import *
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
  def __init__(self,config):
    self.persistent = config.getboolean('Test','save_transposition_table')
    if self.persistent:
      self.table = gdbm.open(config.get('Search', 'transposition_table'),'cf')
    else:
      self.table = {}
  

  def checkCache(self,game_state):
    try:
        return int(self.table[repr(game_state)])
    except KeyError:
        return -1

  def saveToCache(self,game_state,newTricks):
      try:
          oldTricks = int(self.table[repr(game_state)])
          if newTricks > oldTricks:
              self.table[repr(game_state)] = str(newTricks)
      except KeyError:
          self.table[repr(game_state)] = str(newTricks)

  def close(self):
    if self.persistent:
      self.table.close()

if __name__ == '__main__':
  shelve = shelve.open('/home/scratch/tal1/double_dummy/data/transposition_table.dat')
  config = Configuration('search_config.cfg')
  table = config.transTable
  for key,value in shelve.iteritems():
    table.saveToCache(key,value)
  config.close()
  shelve.close()
  
