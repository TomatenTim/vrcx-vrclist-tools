import time

from vrcx import get_latest_vrchat_world_ids
from vrclist import set_world_visited, get_worlds_visited


def main():

    get_worlds_visited()

    while True:

        # get the latest 2 worlds with over 60 sec of visiting time 
        world_ids = get_latest_vrchat_world_ids(min_time=60, count=2)
        
        # sets the worlds to visited on vrclist
        for world_id in world_ids:
            set_world_visited(world_id)
            time.sleep(1)
        
        
        time.sleep(5)
    
if __name__ == '__main__':
    main()
