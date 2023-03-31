from flask import Blueprint, request, jsonify

data_route = Blueprint('product_route', __name__)

'''
TODO:
[ ] - actually execute instead of just returning the inputed information
[ ] - make an endpoint for updating stuff (PUT)
'''

# GET /get_entry/<database>/<entryid>
@data_route.route("/get_entry/<database>/<entryid>", methods=["GET"])
def get_entry(database, entryid):
  return jsonify({'database': database, 'entry': entryid}) 

# GET /query_database/<database>?search_term=value&num_results=value&sort_by=value
@data_route.route("/query_database/<database>", methods=["GET"])
def search_database(database):
  # TODO: this works in the browser but with curl it only returns the first argument
  return request.args 

# POST /create_database/<database>
@data_route.route("/create_database/<database>", methods=["POST"])
def create_datbase(database):
  return f"creating database: {database}\n" 

# POST /create_entry/<database>
@data_route.route("/create_entry/<database>", methods=["POST"])
def create_database_entry(database):
  json = request.json
  return jsonify("created entry: " + str(json))

# DELETE /delete_entry/<database>/<entryid>
@data_route.route("/delete_entry/<database>/<entryid>", methods=["DELETE"])
def delete_database_entry(database, entryid):
  return f"Deleting {database} {entryid}\n" 

