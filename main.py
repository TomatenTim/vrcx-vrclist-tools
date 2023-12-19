import time
from configparser import ConfigParser
import sqlite3

from vrcx import get_latest_vrchat_world_ids
from vrclist import set_world_visited, get_worlds_visited
from localdb import localdb_init

config = ConfigParser()
config.read('config.cfg')

minimal_time = config.getint('VRCListVisited', 'minimal_time', fallback=60)
instance_count = config.getint('VRCListVisited', 'instance_count', fallback=2)


def main():

    localdb_init()
    get_worlds_visited()

    while True:

        # get the latest 2 worlds with over 60 sec of visiting time 
        world_ids = get_latest_vrchat_world_ids(min_time=minimal_time, count=instance_count)
        
        # sets the worlds to visited on vrclist
        for world_id in world_ids:
            set_world_visited(world_id)
            time.sleep(1)
        
        
        time.sleep(5)
    
if __name__ == '__main__':
    main()
