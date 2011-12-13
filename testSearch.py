from configuration import *
from game_state import *
from search import *
from random_deal import Randomhand
from time import clock,time

if __name__ == '__main__':
    config_file = 'search_config.cfg'
    testParams = {"useTable":False,
                  "saveTable":False,
                  "useSingleSuit":False,
                  "sortActions":False}
    normal_config = Search(Configuration(config_file,testParams))
    testParams["useSingleSuit"] = True
    single_suit_config = Search(Configuration(config_file,testParams))
    testParams["useSingleSuit"] = False
    testParams["useTable"] = True
    table_config = Search(Configuration(config_file,testParams))
    testParams["saveTable"] = True
    save_table_config = Search(Configuration(config_file,testParams))
    table = save_table_config.table
    testParams["useSingleSuit"] = True
    all_config = Search(Configuration(config_file,testParams))
    all_config.table.close()
    all_config.table = table
    testParams["sortActions"] = True
    all_sort_config = Search(Configuration(config_file,testParams))
    all_sort_config.table.close()
    all_sort_config.table = table
    for i in range(5,11):
        for j in range(0,1000):
            state = GameState.create_initial(Randomhand(i).deal)

            start_clock = clock()
            start_time = time()
            normal_config.search(state)
            stop_clock = clock() 
            stop_time = time() 
            total_clock = stop_clock - start_clock
            total_time = stop_time - - start_time
            print "%d %d %s %f %f" % (i,j,"n", total_clock, total_time)

            start_clock = clock()
            start_time = time()
            single_suit_config.search(state)
            stop_clock = clock() 
            stop_time = time() 
            total_clock = stop_clock - start_clock
            total_time = stop_time - - start_time
            print "%d %d %s %f %f" % (i,j,"s", total_clock, total_time)

            table_config.table.clear()
            start_clock = clock()
            start_time = time()
            table_config.search(state)
            stop_clock = clock() 
            stop_time = time() 
            total_clock = stop_clock - start_clock
            total_time = stop_time - - start_time
            print "%d %d %s %f %f" % (i,j,"t", total_clock, total_time)

            start_clock = clock()
            start_time = time()
            st = save_table_config.search(state)
            stop_clock = clock() 
            stop_time = time() 
            total_clock = stop_clock - start_clock
            total_time = stop_time - - start_time
            print "%d %d %s %f %f" % (i,j,"st", total_clock, total_time)

            start_clock = clock()
            start_time = time()
            al = all_config.search(state)
            stop_clock = clock() 
            stop_time = time() 
            total_clock = stop_clock - start_clock
            total_time = stop_time - - start_time
            print "%d %d %s %f %f" % (i,j,"al", total_clock, total_time)

            start_clock = clock()
            start_time = time()
            als = all_sort_config.search(state)
            stop_clock = clock() 
            stop_time = time() 
            total_clock = stop_clock - start_clock
            total_time = stop_time - - start_time
            print "%d %d %s %f %f" % (i,j,"als", total_clock, total_time)
