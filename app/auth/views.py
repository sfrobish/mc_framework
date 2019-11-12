from flask import render_template
# from . import db

from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
  # Render the login template on the / route
  return render_template('auth/login_template.html', title="Welcome")

@auth.route('/logout')
def logout():
    return 'Logout'
