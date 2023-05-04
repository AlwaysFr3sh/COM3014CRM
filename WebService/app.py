from flask import Flask, render_template, session, url_for
from flask import redirect, url_for, request
import requests
import json

app = Flask(__name__)

# TODO: do we need proper secret key?
app.secret_key = 'BAD_SECRET_KEY'

# dummy authentication until we implement it 
def authenticate(username:str, password:str):
  return True

@app.route('/')
def hello():
  return render_template("index.html")

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if authenticate(request.form['username'], request.form['password']):
          session['username'] = request.form['username']
          return redirect(url_for('homepage'))
        else:
          error = 'Invalid Credentials. Please try again.'
          
    return render_template('login.html', error=error)

@app.route('/home')
def homepage():
  data = requests.get("http://127.0.0.1:5001/query_collection/toms_test_company") 
  json_data = data.json()
  return render_template('home.html', data=json_data) 

@app.route('/home/<entryid>')
def entrypage(entryid):
  data = requests.get(f"http://127.0.0.1:5001/get_entry/toms_test_company/{entryid}")
  #data = {"phone" : "1234567", "email" : "shithead@gmail.com"}
  json_data = data.json()
  return render_template("entry.html", data=json_data)
  

if __name__ == "__main__":
  app.debug = True
  app.run(port=5002, debug=True)
