from flask import Blueprint, request, flash, jsonify,make_response
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
            resp=jsonify({"message":'Email must have more than 5 letters'})
            resp.status_code=401
        user = User.find_by_email(email)
        company = Company.find_by_ccode(user.ccode)
        
        if user:
            if check_password_hash(user.password, password):
                # user_obj = User(user['_id'], user['email'], user['firstName'], user['lastName'], user['password'], user['secQuestion'], user['answer'])
                resp=make_response({"message" : 'Logged in successfully.', 'cname' : company.cname},200)
                # login_user(user_obj, remember=True)
                # return redirect(url_for('views.feed'))
                
            else:
                resp=jsonify({"message":'Incorrect password, try again!'})
                resp.status_code=401
        else:
            resp=jsonify({"message":'Email does not exist, please sign up to access your account.'})
            resp.status_code=404
        return resp
    return not_found()

@auth.route('/getuser',methods=['GET','[POST]'])
def getuser():
    if request.method == 'POST':
        email = request.json['email']
 
        user = User.find_by_email(email)
        return user

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
            resp=jsonify({"message":'User already exists, Please try logging into your account.'})
            resp.status_code=401
        elif compny:
            resp=jsonify({"message":'Company already exists, try registering on behalf of the company.'})
            resp.status_code=401
        elif len(email) < 5:
            resp=jsonify({"message":'Email must be greater than 4 characters.'})
            resp.status_code=401
        elif len(firstName) < 3:
            resp=jsonify({"message":'First name must be greater than 2 characters.'})
            resp.status_code=401
        elif len(lastName) < 3:
            resp=jsonify({"message":'Second name must be greater than 2 characters.'})
            resp.status_code=401
        elif password1 != password2:
            resp=jsonify({"message":'Password mismatch.'})
            resp.status_code=401
        elif len(password1) < 7:
            resp=jsonify({"message":'Password must be greater than 6 characters.'})
            resp.status_code=401
        elif len(ccode)<5:
            resp=jsonify({"message":"company code cannot be less than 5 characters."})
            resp.status_code=401
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

            resp = jsonify({"message":"User added successfully."})
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
            resp=jsonify({"message":'User already exists, Please try logging into your account.'})
            resp.status_code=401
        elif compny:
            resp=jsonify({"message":'Company already exists, try registering on behalf of the company.'})
            resp.status_code=401
        elif len(email) < 5:
            resp=jsonify({"message":'Email must be greater than 4 characters.'})
            resp.status_code=401
        elif len(firstName) < 3:
            resp=jsonify({"message":'First name must be greater than 2 characters.'})
            resp.status_code=401
        elif len(lastName) < 3:
            resp=jsonify({"message":'Second name must be greater than 2 characters.'})
            resp.status_code=401
        elif password1 != password2:
            resp=jsonify({"message":'Password mismatch.'})
            resp.status_code=401
        elif len(password1) < 7:
            resp=jsonify({"message":'Password must be greater than 6 characters.'})
            resp.status_code=401
        elif len(ccode)<5:
            resp=jsonify({"message":"company code cannot be less than 5 characters."})
            resp.status_code=401
        else:
            password=generate_password_hash(password1, method='sha256')
            answer=generate_password_hash(answer1,method='sha256')
            new_user = User(email,firstName,lastName,
                            password,secQuestion,answer,ccode)
            new_user.save()
           
            # ccode=generate_password_hash(ccode,method='sha256')
            # new_company=Company(comp_code.cname,ccode,comp_code.cinfo,email)
            # new_company.save()

            resp = jsonify({"message":"User added successfully."})
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
            resp=jsonify({"message":"User doesn't exists."})
        elif password1 != password2:
            resp=jsonify({"message"'Password mismatch.'})
        elif len(password1) < 7:
            resp=jsonify({"message"'Password must be greater than 6 characters.'})
        elif secQuestion!=user.secQuestion:
            resp=jsonify({"message""The security question doesn't match."})
        else:
            
            if check_password_hash(user.answer,answer1):
                password=generate_password_hash(password1, method='sha256')
                User.upPass(email,password)
                resp=jsonify({"message""Password updated successfully."})
            else:
                
                resp=jsonify({"message""The security answer verification failed"})
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
