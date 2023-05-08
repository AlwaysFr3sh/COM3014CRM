import pymongo
from flask import make_response, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from utilities.utilities import get_text
import re

# secret = get_text("secret.txt")
# connection_string = "mongodb://localhost:27017/"
# client = pymongo.MongoClient(connection_string)

client = pymongo.MongoClient(host="company_mongo",port=27018,username="root",password="password",authSource="admin")

database_name = "companydb"
database = client[database_name]

def get_many_entries(collection:str, field="", search_term="", num_results=10):
  try:
    collection = database[collection]
    key_regex = re.compile("\w") # the idea is that we don't care what key, we want any key that has value search_term
    #query = {key_regex : search_term} if search_term is not "" else {}
    query = {field : search_term} if field != "" else {}
    result = collection.find(query)
    return dumps(result) + "\n"
  except Exception as e:
    return make_response({"error" : str(e)}, 404)

# create new entry for a given collection
def create_entry(collection_name:str, entry:dict):
  try: 
    collection = database[collection_name]
    result = collection.insert_one(entry)
    if not result.acknowledged:
      raise Exception("Error: Insertion operation not acknowledged")
    return make_response({"message" : f"Successfully inserted item id={result.inserted_id}", "id" : f"{result.inserted_id}"}, 201) 
  except Exception as e:
    return make_response({"error" : str(e)}, 404)

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
    return make_response({"error" : str(e)}, 404)

# This one kinda sucks at the moment, might need more work
def get_entry(collection_name:str, entryid:str):
  try:
    collection = database[collection_name]
    result = collection.find_one({'_id' : ObjectId(entryid)})
    return dumps(result) + "\n"
  except Exception as e:
    return make_response({"error" : str(e)}, 404)


def update_entry(collection_name:str, entryid:str, key:str, value): # TODO: is value ever not string?
  try:
    collection = database[collection_name]
    entry_filter = {"_id" : ObjectId(entryid)}
    newvalues = {"$set" : {key : value}}
    result = collection.update_one(entry_filter, newvalues)
    if not result.acknowledged:
      raise Exception("Error: update operation not acknowledged")
    return make_response({"message" : f"successfully updated item {entryid} key {key} with value {str(value)}"}, 201)
  except Exception as e:
    return make_response({"error" : str(e)}, 404) # TODO: 404 doesn't seem like it'll always be right


'''
TODO:

- Add authentication somewhere
'''

