import pymongo
from flask import make_response, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps

def get_text(path):
  with open(path) as f: text = f.readlines()
  return "".join(text).replace("\n", "")

secret = get_text("secret.txt")
connection_string = f"mongodb+srv://tomhollo123:{secret}@cluster0.fzxqnt6.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
database_name = "test_database"
database = client[database_name]

print(connection_string)

# create new entry for a given collection
def create_entry(collection_name:str, entry:dict):
  try: 
    collection = database[collection_name]
    result = collection.insert_one(entry)
    if not result.acknowledged:
      raise Exception("Error: Insertion operation not acknowledged")
    return make_response({"message" : f"Successfully inserted item id={result.inserted_id}"}, 201) 
  except Exception as e:
    return make_response({"message" : str(e)}, 404)

# delete an entry given an object id
# TODO: might need to write one that takes a dict and runs a delete_one on the supplied dict (received as json)
def delete_entry(collection_name:str, entryid:str):
  try:
    collection = database[collection_name]
    result = collection.delete_one({'_id': ObjectId(entryid)})
    if not result.acknowledged:
      raise Exception("Error: Insertion operation not acknowledged")
    return make_response({"message" : f"Successfully deleted item id={entryid}"}, 201)
  except Exception as e:
    return make_response({"message" : str(e)}, 404)

# This one kinda sucks at the moment, might need more work
def get_entry(collection_name:str, entryid:str):
  try:
    collection = database[collection_name]
    result = collection.find_one({'_id' : ObjectId(entryid)})
    return dumps(result) + "\n"
  except Exception as e:
    return make_response({"message" : str(e)}, 404)


'''
TODO:

- hide our db key somewhere

- Add authentication somewhere
'''

