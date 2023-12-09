import os
import sqlite3

vrcxPath = os.getenv('LOCALAPPDATA')+'\\..\\Roaming\\VRCX'
vrcxDBPath = os.getenv('LOCALAPPDATA')+'\\..\\Roaming\\VRCX\VRCX.sqlite3'



def get_latest_vrchat_world_ids(count = 2, min_time = 0):
    # get the latest x worlds from the VRCX Database
    # with at least <min_time> secounds of visit time

    # check if count and min_time are int
    if(not isinstance(count, int)):
        return

    if(not isinstance(min_time, int)):
        return

    # connect to DB
    connection = sqlite3.connect(vrcxDBPath)
    cursor = connection.cursor()

    # select the data from the vrcx database
    cursor.execute('SELECT world_id FROM gamelog_location WHERE time >= ' + str(min_time * 1000) + ' ORDER BY id DESC LIMIT ' + str(count))

    # get an array with world ids
    worldIDs = set(row[0] for row in cursor.fetchall())

    return worldIDs

