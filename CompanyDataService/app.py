#!/usr/bin/env python3
from flask import Flask
from api.cdata import data_route
import sys

app = Flask("dataservice")
app.register_blueprint(data_route)

@app.route("/", methods=["GET"])
def hello_world():
  return "hello world!!!\n"

if __name__ == "__main__":
  if len(sys.argv) > 1 and sys.argv[1] == "-debug":
    app.debug = True
    app.run(port=5003, debug=True)
  else:
    from waitress import serve
    serve(app, host="0.0.0.0", port=5003)

# https://github.com/Shihara-Dilshan/John-Keells-App-Revamp/tree/main/Server
