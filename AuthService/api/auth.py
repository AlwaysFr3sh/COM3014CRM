from flask import Blueprint, request, flash, redirect, url_for
from flask.templating import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from services.model import User


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if len(email) < 6:
            flash('Email must have more than 5 letters', category='error')
        user = User.get_user_by_email({'email': email})
        if user:
            if check_password_hash(user['password'], password):
                user_obj = User(user['_id'], user['email'], user['firstName'], user['lastName'], user['password'], user['secQuestion'], user['answer'])
                flash('Logged in successfully.', category='success')
                login_user(user_obj, remember=True)
                return redirect(url_for('views.feed'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist, please sign up to access your account.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        lastName=request.form.get('lastName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        secQuestion=request.form.get('question')
        answer=request.form.get('answer')
	cname=request.form.get('company_name')
	cinfo=request.form.get('company_info')
        print(email)
        #print(user.email)
        user = users.find_one({'email': email})

        if user:
            flash('User already exists, Please try logging into your account.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters.', category="error")
        elif len(firstName) < 3:
            flash('First name must be greater than 2 characters.', category="error")
        elif len(lastName) < 3:
            flash('Second name must be greater than 2 characters.', category="error")
        elif password1 != password2:
            flash('Password mismatch.', category="error")
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category="error")
        else:
            new_user = {
                'email': email,
                'firstName': firstName,
                'lastName': lastName,
                'secQuestion': secQuestion,
                'answer': answer,
                'password': generate_password_hash(password1, method='sha256')
            }
            users.insert_one(new_user)
            flash('Account created.', category="success")
            return redirect(url_for('auth.login'))
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
