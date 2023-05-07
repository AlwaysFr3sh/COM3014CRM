#!/usr/bin/env python3
from flask import Flask
import sys
import json
from routes.web import web



app = Flask(__name__)
app.register_blueprint(web)

with open('config.json', 'r') as f:
  config = json.load(f)



# TODO: do we need proper secret key?
app.secret_key = 'BAD_SECRET_KEY'

if __name__ == "__main__":
  if len(sys.argv) > 1 and sys.argv[1] == "-debug":
    app.debug = True
    app.run(port=config["port"], debug=True)
  else:
    from waitress import serve
    serve(app, host="0.0.0.0", port=config["port"])