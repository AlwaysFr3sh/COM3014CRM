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

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
