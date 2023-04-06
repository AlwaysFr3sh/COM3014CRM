from flask import Blueprint, request, jsonify
from services.cdata import create_entry, delete_entry, get_entry

data_route = Blueprint('product_route', __name__)

'''
TODO:
[ ] - make search_database work
[ ] - make an endpoint for updating stuff (PUT or PATCH ?)
[ ] - update language to reflect that each company will have it's own collection in our single database
[ ] - update readme.md to reflect actual implemenation
'''

@data_route.route("/get_entry/<database>/<entryid>", methods=["GET"])
def get_database_entry(database, entryid):
  return get_entry(database, entryid)

# GET /query_database/<database>?search_term=value&num_results=value&sort_by=value
@data_route.route("/query_database/<database>", methods=["GET"])
def search_database(database):
  return request.args 

# TODO: update docs to reflect the fact that we do not need to create collections, it does it automatically
#       if the collection does not exist here
@data_route.route("/create_entry/<database>", methods=["POST"])
def create_database_entry(database):
  return create_entry(database, request.json)

@data_route.route("/delete_entry/<database>/<entryid>", methods=["DELETE"])
def delete_database_entry(database, entryid):
  return delete_entry(database, entryid)

