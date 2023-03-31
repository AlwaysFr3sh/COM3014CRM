from flask import Blueprint, request, jsonify

data_route = Blueprint('product_route', __name__)


# GET /<database>?search_term=value&num_results=value&sort_by=value
@data_route.route("/<database>?search_term=value&num_results=value&sort_by=value", methods=["GET"])
def search_database():
  pass

# GET /<database>/<entry>
@data_route.route("/<database>/<entry>", methods=["GET"])
def get_entry(database, entry):
  return jsonify({'database': database, 'entry': entry}) 

# POST /<database>
@data_route.route("/<database>", methods=["GET"])
def create_datbase():
  args = request.args
  print(args)

# POST /<database>/<entry>
@data_route.route("/<database>/<entry>", methods=["POST"])
def create_database_entry():
  args = request.args
  print(args)

# DELETE /<database>/<entry>
@data_route.route("/<database>/<entry>", methods=["DELETE"])
def delete_database_entry():
  args = request.args
  print(args)

