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
          session['company'] = 'toms_test_company'
          return redirect(url_for('homepage'))
        else:
          error = 'Invalid Credentials. Please try again.'
          
    return render_template('login.html', error=error)

@app.route('/home')
def homepage():
  data = requests.get(f"http://127.0.0.1:5001/query_collection/{session['company']}") 
  json_data = data.json()
  return render_template('home.html', data=json_data) 

@app.route('/home/<entryid>', methods=['GET', 'POST'])
def entrypage(entryid):
  data = requests.get(f"http://127.0.0.1:5001/get_entry/{session['company']}/{entryid}")
  #data = {"phone" : "1234567", "email" : "shithead@gmail.com"}
  json_data = data.json()

  if request.method == 'POST':
    # Get data from form
    new_data = request.form
    # Compare to our old data
    # we convert json values() object to list and subscript 1-n to avoid the _id which the form doesn't have
    for key, old_value, new_value in zip(new_data.keys(), list(json_data.values())[1:], new_data.values()):
      print(old_value, new_value)
      if old_value != new_value:
        params = {"entry_key" : key ,"entry_value" : new_value}
        # patch the different data in
        requests.patch(f"http://127.0.0.1:5001/update_entry/toms_test_company/{entryid}", params=params)
        # Update our local value to reflect change made to the database
        json_data[key] = new_value

  return render_template("entry.html", data=json_data)
  

if __name__ == "__main__":
  app.debug = True
  app.run(port=5002, debug=True)
