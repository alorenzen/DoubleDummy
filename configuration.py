import ConfigParser

from relative_rank import RelativeRank
from single_suit import *
from transposition_tables import *

class Configuration:
    def __init__(self,config_file,test_params={}):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        if test_params:
            self.useTable = test_params["useTable"]
            self.saveTable = test_params["saveTable"]
            self.useSingleSuit = test_params["useSingleSuit"]
            self.sortActions = test_params["sortActions"]
        else:
            self.useTable = self.config.getboolean('Test','transposition_table')
            self.saveTable = self.config.getboolean('Test','save_transposition_table')
            self.useSingleSuit = self.config.getboolean('Test','single_suit')
            self.sortActions = self.config.getboolean('Test','sort_actions')
        if self.useTable:
            self.transTable = TranspositionTable(self.config,self.saveTable)
        if self.useSingleSuit:
            self.rank = RelativeRank(self.config)
            self.singleSuit = SingleSuit(self.config,self.rank)

    def close(self):
        if self.useTable:
            self.transTable.close()
        if self.useSingleSuit:
            self.rank.close()
            self.singleSuit.close()

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.add_section('Search')
    config.add_section('Test')
    default_folder = '/home/scratch/tal1/double_dummy/data/'
    config.set('Search', 'transposition_table', default_folder + 'transposition.data')
    config.set('Search', 'relative_rank',       default_folder + 'relative_rank.dat' )
    config.set('Search', 'single_suit',         default_folder + 'single_suit.dat'   )
    config.set('Test',   'transposition_table',      'true')
    config.set('Test',   'save_transposition_table', 'true')
    config.set('Test',   'single_suit',              'true')
    config.set('Test',   'sort_actions',             'true')

    with open('search_config.cfg', 'wb') as configfile:
        config.write(configfile)

    
