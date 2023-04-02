"""
A companies data will be stored as a collection within our single database

I'm not sure of the security implications here, but my intuition tells me 
if this was a real product we were making it would be best to separate the data into completely separate
databases.

But that sounds too hard for a uni project. 
"""
import pymongo
from flask import make_response
from bson.objectid import ObjectId

connection_string = "mongodb+srv://tomhollo123:YxFVZ0FYVKA7ccih@cluster0.fzxqnt6.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
database_name = "test_database"
database = client[database_name]

# create new entry for a given collection
def create_entry(collection_name: str, entry: dict):
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
def delete_entry(collection_name: str, entryid: str):
  try:
    collection = database[collection_name]
    result = collection.delete_one({'_id': ObjectId(entryid)})
    if not result.acknowledged:
      raise Exception("Error: Insertion operation not acknowledged")
    return make_response({"message" : f"Successfully deleted item id={entryid}"}, 201)
  except Exception as e:
    return make_response({"message" : str(e)}, 404)
