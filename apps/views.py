# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import Flask, render_template, request, flash, redirect, url_for, jsonify
from jinja2  import TemplateNotFound
from .models import *
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from random import sample 
from .controller import controller
from apps import app

import re

def is_valid_string(s): # Check that the given string is a valid email  
    pattern = r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{3}$'
    return bool(re.match(pattern, s))

@app.route('/')
def route_default():
    return redirect(url_for('login'))

# Login & Registration

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # read form data
        username = request.form.get('Username')
        password = request.form.get('Password')
        
        # Locate user
        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('route_default'))
            else:
                return render_template('accounts/login.html',
                               msg='Wrong password')
        else:
            return render_template('accounts/login.html',
                               msg=' User not found or wrong user')

    if not current_user.is_authenticated:
        return render_template('accounts/login.html')
    return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check usename exists
        user = Users.query.filter_by(username=username).first()

        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False)
        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False)


        if email == "":
            return render_template('accounts/register.html',
                                   msg='Email field can not be empty',
                                   success=False)
        elif not is_valid_string(email):
            return render_template('accounts/register.html',
                                   msg='Not a Valid Email',
                                   success=False)
        
        if username =="" :
            return render_template('accounts/register.html',
                                   msg='Username field can not be empty',
                                   success=False)
        
        new_user = controller.addUser(username = username ,email=email, password= generate_password_hash(password, method='sha256'))
        login_user(new_user, remember=True)


        return redirect(url_for('route_default'))
    
    return render_template('accounts/register.html')
       
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
    

@app.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


