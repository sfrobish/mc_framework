from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from . import auth
from ..models import user

@auth.route('/login')
def login():
  # Render the login template on the / route
  return render_template('auth/login_template.html', title="Welcome")

@auth.route('/login', methods=['POST'])
def login_post():
  email = request.form.get('email')
  password = request.form.get('password')
  # remember = True if request.form.get('remember') else False

  found_user = user.query.filter_by(user_email=email).first()
  
  # check if user actually exists
  # take the user supplied password, hash it, and compare it to the hashed password in database
  # if not user or not check_password_hash(user.password, password): 
  if not found_user or not found_user.user_password_digest == password: 
    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

  # if the above check passes, then we know the user has the right credentials
  login_user(found_user)
  return redirect(url_for('home.homepage'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
