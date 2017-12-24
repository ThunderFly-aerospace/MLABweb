#
#
#   Skrypt, ktery projde projektove JSON soubory a vlozi je do MONGODB
#
#

import os
import json
import pymongo


db = pymongo.MongoClient("localhost", 27017).MLABweb


'''
for root, dirs, files in os.walk('/data/Modules/'):
    for name in files:
        if name.endswith((".json")):
            #print os.path.join(root, name)
            
            json_data=open(os.path.join(root,name)).read()
            data = json.loads(json_data)
            #print data
            #data['_id'] = data['name']
            print os.path.dirname(root)[14:]
            #print os.path.pathname(root)
            id_data = os.path.dirname(root)[14:]
            #try:
            print data
            print data['name']

            db.Modules.update({"_id":data['name']}, data, upsert=True)
            
            #db.Modules.update({"_id":data['name']},{"$set":{"root":root[14:]}})
          #  db.Modules.update({"_id":id_data},{"$set":{"root":root[14:], "":}})
            
            #
            db.Modules.update({"_id": data['name']},{"$set":{"mark":50}})
            #db.Modules.update({"_id": data['name']},{"$unset":{"status":""}})

            #except Exception as e:
            #    print e
'''

for el in db.Modules.find():
    print el.get('author[]'), type(el.get('author[]')), isinstance(el.get('author[]'), unicode), el['_id']
    if isinstance(el.get('author[]'), unicode):
        db.Modules.update({"_id": el['_id']}, {"$set":{'author[]': [el.get('author[]')] }})