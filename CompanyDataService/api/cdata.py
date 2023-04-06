from flask import Blueprint, request, jsonify
from services.cdata import create_entry, delete_entry, get_entry, search

data_route = Blueprint('product_route', __name__)

'''
TODO:
[ ] - make search_collection work
[ ] - make an endpoint for updating stuff (PUT or PATCH ?)
[ ] - update language to reflect that each company will have it's own collection in our single collection
[ ] - update readme.md to reflect actual implemenation
'''

@data_route.route("/get_entry/<colname>/<entryid>", methods=["GET"])
def get_collection_entry(colname, entryid):
  return get_entry(colname, entryid)

# GET /query_collection/<collection>?search_term=value&num_results=value&sort_by=value
# if you curl this method with no kwargs, you need to at a '\' or a ' ' to the end to escape the return key press
# Returns everything from that collection if search term and field are not specified
# TODO: call find with the query value as a regex (\w) if no search_term is specified 
# TODO: we are not doing num_results anymore 
@data_route.route("/query_collection/<colname>", methods=["GET"])
def search_collection(colname):
  #return request.args 
  if 'field' in request.args.keys() and 'search_term' in request.args.keys():
    field, search_term = request.args['field'], request.args['search_term']
    ret = search(colname, field=field, search_term=search_term)
  else:
    ret = search(colname)
    
  return ret
  #return search(colname, request.args['search_term'])

# TODO: update docs to reflect the fact that we do not need to create collections, it does it automatically
#       if the collection does not exist here
@data_route.route("/create_entry/<colname>", methods=["POST"])
def create_collection_entry(colname):
  return create_entry(colname, request.json)

@data_route.route("/delete_entry/<colname>/<entryid>", methods=["DELETE"])
def delete_collection_entry(colname, entryid):
  return delete_entry(colname, entryid)

