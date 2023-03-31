#!/usr/bin/env python3
from flask import Flask
from api.cdata import data_route

app = Flask("dataservice")
app.register_blueprint(data_route)

@app.route("/", methods=["GET"])
def hello_world():
  return "hello world!!!"

if __name__ == "__main__":
  app.debug = True
  app.run(port=5001, debug=True)

# https://github.com/Shihara-Dilshan/John-Keells-App-Revamp/tree/main/Server
