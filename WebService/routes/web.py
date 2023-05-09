from flask import render_template, session, url_for, redirect, request, Blueprint

import requests
import json


web = Blueprint('web', __name__)

with open('config.json', 'r') as f:
  config = json.load(f)

@web.route('/')
def hello():
  return render_template("index.html",user=session)

# dummy authentication until we implement it 
def authenticate(email:str, password:str):
  user_credentials={"email":email,"password":password}
  login=requests.post(f"{config['auth_service_url']}/login",json=user_credentials,timeout=10)
  
  authenticated = login.status_code==200
  status=login.status_code
  company_name = login.json()['message']
  if authenticated:
    company_name = login.json()['cname']
    
    
  return authenticated, company_name,status



# Route for handling the login page logic
@web.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    status=None
    if request.method == 'POST':
        authenticated, company_name, status= authenticate(request.form['email'], request.form['password'])
        #if authenticate(request.form['username'], request.form['password']):
        
        print(company_name)
        if authenticated:
          session['email'] = request.form['email']
          session['company'] = company_name
          
          
          return redirect(url_for('web.homepage'))
        else:
          error = company_name
          
    return render_template('login.html', error=error,status=status,user=session)

@web.route('/signup',methods=['GET','POST'])
def signup():
  error=None
  status=None
  if request.method== 'POST':
    entry = dict(request.form)
    signin=requests.post(f"{config['auth_service_url']}/signup", json=entry,timeout=10)
    status=signin.status_code
    message=signin.json()['message']
    if signin.status_code==200:
      return render_template('login.html',error=message,status=status,user=session)
    else:
      error=message
  return render_template("signup.html",error=error,status=status,user=session)
        
@web.route('/signupcompany',methods=['GET','POST'])
def signupcompany():
  error=None
  status=None
  if request.method== 'POST':
    entry = dict(request.form)
    signin=requests.post(f"{config['auth_service_url']}/signupcompany", json=entry,timeout=10)
    status=signin.status_code
    message=signin.json()['message']
    if signin.status_code==200:
      return render_template('login.html',error=message,status=status)
    else:
      error=message
  return render_template("signupcompany.html",error=error,status=status,user=session)

@web.route('/forgotPass',methods=['GET','POST'])
def updatePass():
  error=None
  status=None
  if request.method=='POST':
    entry=dict(request.form)
    updateP=requests.post(f"{config['auth_service_url']}/updatePass",json=entry)
    message=updateP.json()['message']
    status=updateP.status_code
    if updateP.status_code==200:
      return render_template('forgotPass.html',error=message,status=status,user=session)
    else:
      error=message
  return render_template("forgotPass.html",error=error,status=status,user=session)

@web.route('/home')
def homepage():
  if session.get('email'):
    data = requests.get(f"{config['data_service_url']}/query_collection/{session['company']}") 
    json_data = data.json()
    ret = render_template('home.html', data=json_data,user=session) 
  else:
    ret = render_template('home.html',user=session)
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
        requests.patch(f"{config['data_service_url']}/update_entry/toms_test_company/{entryid}", params=params)
        # Update our local value to reflect change made to the database
        json_data[key] = new_value

  return render_template("entry.html", data=json_data,user=session)


@web.route('/new', methods = ['GET', 'POST'])
def new_entry():
  user=session.get('email')
  if user and request.method == 'POST':
    entry = dict(request.form)
    requests.post(f"{config['data_service_url']}/create_entry/{session['company']}", json=entry)
    return redirect(url_for('web.homepage'))
  return render_template("new_entry.html", data=config["default_fields"],user=session)
  
@web.route('/delete_entry/<entryid>')
def delete_entry(entryid):
  requests.delete(f"{config['data_service_url']}/delete_entry/{session['company']}/{entryid}")
  return redirect(url_for('web.homepage'),user=session)

@web.route('/about')
def about():
  return render_template("about.html",user=session)

@web.route('/logout')
def log_out():
  session.pop('email')
  session.pop('company')
  return redirect(url_for('web.homepage'))