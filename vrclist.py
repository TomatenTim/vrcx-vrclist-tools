from configparser import ConfigParser
import requests

from localdb import add_vrcx_vrclist_id_relation, resolve_vrclist_id, resolve_vrcx_id

config = ConfigParser()
config.read('config.cfg')

vrclist_uuid = config['VRCList']['uuid']

cache_worlds_visited = []

def send_api_request(path, payload=None): 
    # send an authenticated request to VRCList

    url = 'https://api.vrclist.com' + path
    cookies = { "uuid": vrclist_uuid }


    if(payload):
        response = requests.post(url,  cookies=cookies, json=payload)
    else:
        response = requests.get(url,  cookies=cookies)

    return response


# search world by vrcx_id 
def search_vrclist_id_by_vrcx_id(vrcx_id): 
    
    if(not vrcx_id):
        return
    
    vrclist_id = resolve_vrcx_id(vrcx_id)

    if(vrclist_id):
      return vrclist_id

    res = send_api_request('/worlds/search', {
        "name_author_id": vrcx_id,
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
            vrclist_id = world_data['id']
            add_vrcx_vrclist_id_relation(vrcx_id=vrcx_id, vrclist_id=vrclist_id)
            return vrclist_id
  
    return


def set_world_visited(vrcx_id): 
    # sets a world to visited with the given vrchat_world_id

    # get world info from vrclist 
    vrclist_id = search_vrclist_id_by_vrcx_id(vrcx_id)

    if(not vrclist_id):
        # TODO: log if world not found
       return

    # check if the world was already visited since program start
    if(vrclist_id in cache_worlds_visited):
        return


    # send the request to set the world to visited
    res = send_api_request('/user/visited', {
        "world_id": vrclist_id,
        # "world_name": world_data['name']
    })

    # if worked store that to prevent sending it again
    if(res.status_code == 200):
        print('VRCList: Set world "' + vrcx_id + '" to visited')
        cache_worlds_visited.append(vrclist_id)


def get_worlds_visited():
    res = send_api_request('/user/visited')

    data = res.json()

    for world_data in data:
        cache_worlds_visited.append(world_data['world_id'])
