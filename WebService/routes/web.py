from flask import render_template, session, url_for, redirect, request, Blueprint
import requests
import json

web = Blueprint('web', __name__)

with open('config.json', 'r') as f:
  config = json.load(f)


# dummy authentication until we implement it 
def authenticate(email:str, password:str):
  user_credentials={"email":email,"password":password}
  login=requests.post(f"{config['auth_service_url']}/login",json=user_credentials)
  authenticated = login.status_code==200
  company_name = ""
  if authenticated:
    company_name = login.json()['cname']
  
  return authenticated, company_name

@web.route('/')
def hello():
  return render_template("index.html")

# Route for handling the login page logic
@web.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        authenticated, company_name = authenticate(request.form['username'], request.form['password'])
        #if authenticate(request.form['username'], request.form['password']):
        print(company_name)
        if authenticated:
          session['username'] = request.form['username']
          session['company'] = company_name
          
          return redirect(url_for('web.homepage'))
        else:
          error = 'Invalid Credentials. Please try again.'
          
    return render_template('login.html', error=error)

@web.route('/home')
def homepage():
  if session.get('username'):
    data = requests.get(f"{config['data_service_url']}/query_collection/{session['company']}") 
    json_data = data.json()
    ret = render_template('home.html', data=json_data) 
  else:
    ret = render_template('home.html')
  return ret

@web.route('/home/<entryid>', methods=['GET', 'POST'])
def entrypage(entryid):
  data = requests.get(f"{config['data_service_url']}/get_entry/{session['company']}/{entryid}")
  json_data = data.json()

  if request.method == 'POST':
    # Get data from form
    new_data = request.form
    # Compare to our old data
    # we convert json values() object to list and subscript 1-n to avoid the _id which the form doesn't have
    for key, old_value, new_value in zip(new_data.keys(), list(json_data.values())[1:], new_data.values()):
      if old_value != new_value:
        params = {"entry_key" : key ,"entry_value" : new_value}
        # patch the different data in
        requests.patch(f"{config['data_service_url']}/update_entry/{session['company']}/{entryid}", params=params)
        # Update our local value to reflect change made to the database
        json_data[key] = new_value

  return render_template("entry.html", data=json_data)


@web.route('/new', methods = ['GET', 'POST'])
def new_entry():
  if request.method == 'POST':
    entry = dict(request.form)
    requests.post(f"{config['data_service_url']}/create_entry/{session['company']}", json=entry)
    return redirect(url_for('web.homepage'))
  return render_template("new_entry.html", data=config["default_fields"])
  
@web.route('/delete_entry/<entryid>')
def delete_entry(entryid):
  requests.delete(f"{config['data_service_url']}/delete_entry/{session['company']}/{entryid}")
  return redirect(url_for('web.homepage'))

@web.route('/logout')
def log_out():
  session.pop('username')
  session.pop('company')
  return redirect(url_for('web.homepage'))