from flask import Blueprint, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from services.model import User
from services.model import Company


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        if len(email) < 6:
            resp=jsonify('Email must have more than 5 letters')
        user = User.find_by_email(email)
        
        if user:
            if check_password_hash(user.password, password):
                # user_obj = User(user['_id'], user['email'], user['firstName'], user['lastName'], user['password'], user['secQuestion'], user['answer'])
                resp=jsonify('Logged in successfully.')
                # login_user(user_obj, remember=True)
                # return redirect(url_for('views.feed'))
            else:
                resp=jsonify('Incorrect password, try again!')
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
        secQuestion=request.json['secQuestion']
        answer1=request.json['answer']
        cname=request.json['cname']
        ccode=request.json['ccode']
        cinfo=request.json['cinfo']
        
        user=User.find_by_email(email)
        compny=Company.find_by_ccode(ccode)
        if user:
            resp=jsonify('User already exists, Please try logging into your account.')
        elif compny:
            resp=jsonify('Company already exists, try registering on behalf of the company.')
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
        elif len(ccode)<5:
            resp=jsonify("company code cannot be less than 5 characters.")
        else:
            password=generate_password_hash(password1, method='sha256')
            #Should we add ccode in User database as well to connect the databases.
            answer=generate_password_hash(answer1,method='sha256')
            new_user = User(email,firstName,lastName,
                            password,secQuestion,answer,ccode)
            new_user.save()
           
            # ccode=generate_password_hash(ccode,method='sha256')
            # Thought of hashing the ccode but it gets difficult to retrieve the company details using the companycode then.
            # Everytime we hash a text it returns a different string 
            new_company=Company(cname,ccode,cinfo)
            new_company.save()

            resp = jsonify("User added successfully.")
            resp.status_code=200
        return resp
    else:
        return not_found()
    
@auth.route('/signupcompany',methods=['GET','POST'])
def csignup():
    if request.method=='POST':
        email=request.json['email']
        firstName=request.json['firstName']
        lastName=request.json['lastName']
        password1=request.json['password1']
        password2=request.json['password2']
        secQuestion=request.json['secQuestion']
        answer1=request.json['answer']
        ccode=request.json['ccode']
        
        user=User.find_by_email(email)
        compny=Company.find_by_ccode(ccode)
        #TO-DO: Figure out whether same email id can be associated with multiple comapnies or not
        if user:
            resp=jsonify('User already exists, Please try logging into your account.')
        elif compny is None:
            resp=jsonify('Invalid company code!')
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
        elif len(ccode)<5:
            resp=jsonify("company code cannot be less than 5 characters.")
        else:
            password=generate_password_hash(password1, method='sha256')
            answer=generate_password_hash(answer1,method='sha256')
            new_user = User(email,firstName,lastName,
                            password,secQuestion,answer,ccode)
            new_user.save()
           
            # ccode=generate_password_hash(ccode,method='sha256')
            # new_company=Company(comp_code.cname,ccode,comp_code.cinfo,email)
            # new_company.save()

            resp = jsonify("User added successfully.")
            resp.status_code=200
        return resp
    else:
        return not_found()
    
@auth.route('/updatePass',methods=['GET','POST'])
def updatePass():
    if request.method=='POST':
        email=request.json['email']
        secQuestion=request.json['secQuestion']
        answer1=request.json['answer']
        password1=request.json['password1']
        password2=request.json['password2']
        user=User.find_by_email(email)

        if user is None:
            resp=jsonify("User doesn't exists.")
        elif password1 != password2:
            resp=jsonify('Password mismatch.')
        elif len(password1) < 7:
            resp=jsonify('Password must be greater than 6 characters.')
        elif secQuestion!=user.secQuestion:
            resp=jsonify("The security question doesn't match.")
        else:
            
            if check_password_hash(user.answer,answer1):
                password=generate_password_hash(password1, method='sha256')
                User.upPass(email,password)
                resp=jsonify("Password updated successfully.")
            else:
                
                resp=f"The security answer verification failed.{user.answer}"
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
