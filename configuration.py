import ConfigParser

from relative_rank import RelativeRank
from single_suit import *
from transposition_tables import *

class Configuration:
    def __init__(self,config_file):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self.transTable = TranspositionTable(self.config)
        self.rank = RelativeRank(self.config)
        self.singleSuit = SingleSuit(self.config,self.rank)

    def close(self):
        self.transTable.close()
        self.rank.close()
        self.singleSuit.close()

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.add_section('Search')
    default_folder = 'data/'
    config.set('Search','transposition_table', default_folder + 'transposition.data')
    config.set('Search', 'relative_rank', default_folder + 'relative_rank.dat')
    config.set('Search','single_suit', default_folder + 'single_suit.dat')

    with open('search_config.cfg', 'wb') as configfile:
        config.write(configfile)

    
