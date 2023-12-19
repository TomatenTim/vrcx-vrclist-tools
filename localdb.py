import os
import sqlite3
from datetime import datetime


db_file = './data/db.sqlite'

def localdb_init():
    db_dir = os.path.dirname(db_file)
    if (not os.path.exists(db_dir)):
        os.mkdir(db_dir)
    
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # create the vrcx vrclist id relationsship table
    cursor.execute('CREATE TABLE IF NOT EXISTS "vrcx_vrclist_ids" ('+
                        'id INTEGER PRIMARY KEY, ' +
                        'vrcx_id TEXT NOT NULL, ' +
                        'vrclist_id INTEGER NOT NULL, ' +
                        'date_added TEXT NOT NULL ' +
                    ');'
    )

    cursor.close()

# adds a new id relation and deletes old ones with the same 
# vrcx_id or vrclist_id to avoid dublicates
def add_vrcx_vrclist_id_relation(vrcx_id, vrclist_id):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # select all relations with the same vrcx and vrclist id
    cursor.execute('SELECT id, vrcx_id, vrclist_id FROM vrcx_vrclist_ids WHERE vrcx_id = ? OR vrclist_id = ?;', 
                    (vrcx_id, vrclist_id))

    relations = cursor.fetchall()

    # if length is not 1 
    # or length is 1 and the ids are not matching
    # -> delete all selected
    if (len(relations) != 1 or list(relations[0])[1] != vrcx_id or list(relations[0])[2] != vrclist_id):
        
        relation_ids = set(str(row[0]) for row in relations)
        # if is are there any ids delete them
        if(len(relation_ids) != 0):
            cursor.execute('DELETE FROM vrcx_vrclist_ids WHERE id IN(' + ','.join(relation_ids) + ');')

        date = str(datetime.now())

        # add new relation to the database
        cursor.execute('INSERT INTO vrcx_vrclist_ids (vrcx_id, vrclist_id, date_added) VALUES (?,?,?);',
                        (vrcx_id, vrclist_id, date))
        
        connection.commit()

        cursor.close()
        connection.close()

# resolve a vrcx id to a vrclist id using the local db
def resolve_vrcx_id(vrcx_id):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('SELECT vrclist_id FROM vrcx_vrclist_ids WHERE vrcx_id = ?;', (vrcx_id,))

    vrclist_ids = list(set(row[0] for row in cursor.fetchall()))

    cursor.close()
    if (len(vrclist_ids) == 1):
        return vrclist_ids[0]
    return

# resolve a vrclist id to a vrcx id using the local db
def resolve_vrclist_id(vrclist_id):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('SELECT vrcx_id FROM vrcx_vrclist_ids WHERE vrclist_id = ?;', (vrclist_id,))

    vrcx_ids = list(set(row[0] for row in cursor.fetchall()))

    cursor.close()
    if (len(vrcx_ids) == 1):
        return vrcx_ids[0]
    return
