from flask import Blueprint, request, flash, jsonify
from flask.templating import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from services.model import User


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        if len(email) < 6:
            resp=jsonify('Email must have more than 5 letters')
        user = User.find_by_email(email)
        print(user)
        if user:
            if check_password_hash(user.password, password):
                # user_obj = User(user['_id'], user['email'], user['firstName'], user['lastName'], user['password'], user['secQuestion'], user['answer'])
                resp=jsonify('Logged in successfully.')
                # login_user(user_obj, remember=True)
                # return redirect(url_for('views.feed'))
            else:
                resp=jsonify(f'Incorrect password, try again!{user.password}')
        else:
            resp=jsonify('Email does not exist, please sign up to access your account.')
        return resp
    return not_found()

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.json['email']
        firstName=request.json['firstName']
        lastName=request.json['lastName']
        password1=request.json['password1']
        password2=request.json['password2']
        # secQuestion=request.json.get('question')
        # answer=request.json.get('answer')
        # cname=request.json.get('company_name')
        # cinfo=request.json.get('company_info')
        #print(user.email)
        user=User.find_by_email(email)

        if user:
            resp=jsonify('User already exists, Please try logging into your account.')
        elif len(email) < 5:
            resp=jsonify('Email must be greater than 4 characters.')
        elif len(firstName) < 3:
            resp=jsonify('First name must be greater than 2 characters.')
        elif len(lastName) < 3:
            resp=jsonify('Second name must be greater than 2 characters.')
        elif password1 != password2:
            resp=jsonify('Password mismatch.')
        elif len(password1) < 7:
            resp=jsonify('Password must be greater than 6 characters.')
        else:
            new_user = User(email,firstName,lastName,password=generate_password_hash(password1, method='sha256'))
            new_user.save()
            resp = jsonify("User added successfully.")
            resp.status_code=200
        return resp
    else:
        return not_found()
    
@auth.errorhandler(404)
def not_found(erron=None):
    message={
        'status':404,
        'message':'Not Found'+request.url
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp

# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))
