#!/usr/bin/env python3
import requests
from flask import Flask, make_response
from random import choice
import json
app = Flask(__name__)

with open('config.json', 'r') as f:
  config = json.load(f)

def hash_choose(colname):
  return hash(colname) % len(config['backends'])

# The way I designed the endpoints for the data service sucks :(
@app.route("/query_collection/<colname>", methods=["GET"])
def query_collection(colname):
  choice = hash_choose(colname)
  return requests.get(f"http://{config['backends'][choice]}/query_collection/{colname}").json() 

@app.route("/get_entry/<colname>/<entryid>", methods=["GET"])
def get_entry(colname, entryid):
  choice = hash_choose(colname)
  return requests.get(f"http://{choice(config['backends'][choice])}/get_entry/{colname}/{entryid}") 

@app.route("/create_entry/<colname>", methods=["POST"])
def create_entry(colname):
  choice = hash_choose(colname)
  return requests.post(f"http://{choice(config['backends'][choice])}/create_entry/{colname}")

@app.route("/delete_entry/<colname>/<entryid>", methods=["DELETE"])
def delete_entry(colname, entryid):
  choice = hash_choose(colname)
  return requests.delete(f"http://{choice(config['backends'][choice])}/delete_entry/{colname}/{entryid}")

@app.route("/update_entry/<colname>/<entryid>", methods=["PATCH"])
def update_entry(colname, entryid):
  choice = hash_choose(colname)
  return requests.patch(f"http://{choice(config['backends'][choice])}/update_entry/{colname}/{entryid}")

if __name__ == "__main__":
  port = config["port"]
  app.debug = True
  app.run(port=port, debug=True)
