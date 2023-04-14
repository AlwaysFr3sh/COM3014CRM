from flask import Blueprint, request, jsonify
from services.cdata import create_entry, delete_entry, get_entry, get_many_entries, update_entry

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
# TODO: fuzzy search, is it possible to ask mongodb to find documents containing a value without specifying a key
#       this could be acheived in the future by storing a document containing all of the keys used in a collection
#       and performing the find() query for each of them, this sounds like too much work so it's something for after
#       the frontend is at least partially up and running
# TODO: we are not doing num_results anymore... or are we???
@data_route.route("/query_collection/<colname>", methods=["GET"])
def search_collection(colname):
  #return request.args 
  field_and_searchterm = 'field' in request.args.keys() and 'search_term' in request.args.keys()
  searchterm_only = 'field' not in request.args.keys() and 'search_term' in request.args.keys()
  #if 'field' in request.args.keys() and 'search_term' in request.args.keys():
  if field_and_searchterm:
    field, search_term = request.args['field'], request.args['search_term']
    ret = get_many_entries(colname, field=field, search_term=search_term)
  elif searchterm_only:
    ret = {"message" : "this is not implemented yet bro"}
  else:
    ret = get_many_entries(colname)
    
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

#/update_entry/<colname>/<entryid>?entry_key=value&entry_value=value
@data_route.route("/update_entry/<colname>/<entryid>", methods=["PATCH"]) # I don't think we need a PUT
def update_collection_entry(colname, entryid):
  # TODO: some error handling here might be good?
  key, value = request.args['entry_key'], request.args['entry_value']
  return update_entry(colname, entryid, key, value)

