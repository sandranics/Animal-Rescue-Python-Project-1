from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   #means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST']) #what types of request can be accepted - GET and POST
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #filter all users with this email
        if user:
            if check_password_hash(user.password, password):  
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #remembers the user is logged in
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() 
        if user: #Checks if data is valid
            flash('Този имейл вече съществува.', category='error') #a functon used to flash messages in flask
        elif len(email) < 4:
            flash('Имейлът Ви трябва да е по-дълъг от 3 знака.', category='error')
        elif len(first_name) < 2:
            flash('Името Ви трябва да е по-дълго от 1 знак.', category='error')
        elif password1 != password2:
            flash('Паролите не съвпадат.', category='error')
        elif len(password1) < 7:
            flash('Паролата Ви трябва да е поне 7 знака.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit() #updates the database
            login_user(new_user, remember=True)
            flash('Създаден акаунт.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
