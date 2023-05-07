from flask import Flask
# from services.model import app
# from init import create_app
from api.auth import auth
#from __init__ import db

app = Flask(__name__)



app.register_blueprint(auth)

if __name__ == '__main__':
    #db.create_all() 
    app.run(debug=True,port=5001,host='0.0.0.0') 
    