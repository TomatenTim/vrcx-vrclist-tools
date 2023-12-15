from configparser import ConfigParser
import requests

config = ConfigParser()
config.read('config.cfg')

vrclist_uuid = config['VRCList']['uuid']

cache_world_id = {}
cache_worlds_visited = []

def send_api_request(path, payload=None): 
    # send an authenticated request to VRCList

    url = 'https://api.vrclist.com' + path
    cookies = { "uuid": vrclist_uuid }

    print('req', url, payload)


    if(payload):
        response = requests.post(url,  cookies=cookies, json=payload)
    else:
        response = requests.get(url,  cookies=cookies)

    return response



def search_world_by_id(vrchat_world_id): 
    # search world by vrchat_world_id 

    if(vrchat_world_id in cache_world_id):
        return cache_world_id[vrchat_world_id]

    res = send_api_request('/worlds/search', {
        "name_author_id": vrchat_world_id,
        "tags": "",
        "sort": "recent",
        "exclude_visited": False,
        "quest_only": False,
        "page": 0
    })

    if(res.status_code == 200):
        json = res.json()

        if(len(json) != 0):
            world_data = json[0]
            cache_world_id[world_data['world_id']] = world_data
            return world_data
  
    return


def set_world_visited(vrchat_world_id): 
    # sets a world to visited with the given vrchat_world_id

    # get world info from vrclist 
    world_data = search_world_by_id(vrchat_world_id)

    if(not world_data):
        # TODO: log if world not found
       return

    # check if the world was already visited since program start
    if(world_data['id'] in cache_worlds_visited):
        return


    # send the request to set the world to visited
    res = send_api_request('/user/visited', {
        "world_id": world_data['id'],
        "world_name": world_data['name']
    })

    # if worked store that to prevent sending it again
    if(res.status_code == 200):
        cache_worlds_visited.append(world_data['id'])


def get_worlds_visited():
    res = send_api_request('/user/visited')

    data = res.json()

    for world_data in data:
        cache_worlds_visited.append(world_data['world_id'])
