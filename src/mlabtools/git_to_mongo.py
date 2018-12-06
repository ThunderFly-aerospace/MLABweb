#
#
#   Skript, ktery projde projektove JSON soubory a vlozi je do MONGODB
#
#

import os
import json
import pymongo


db = pymongo.MongoClient("localhost", 27017).MLABweb



for root, dirs, files in os.walk('/data/mlab/Modules/'):
    for name in files:
        if name.endswith((".json")):
            print("......")
            #print os.path.join(root, name)
            
            json_data=open(os.path.join(root,name)).read()
            data = json.loads(json_data)
            print os.path.dirname(root)[19:]
            id_data = os.path.dirname(root)[19:]
            #try:
            print data
            print data['name']

            if not data.get('mark', False):
                data['mark'] = 50

            if not type(data['category[]']) == list:
                data['category[]'] = [data['category[]']]

            db.Modules.update({"_id":data['name']}, data, upsert=True)