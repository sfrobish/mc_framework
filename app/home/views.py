from flask import abort, flash, redirect, render_template, url_for
from . import home

@home.route('/', methods=['GET', 'POST'])
def homepage():
  
  # Render the homepage template on the / route
  return render_template('home/index.html', title="Welcome")


@home.route('/control/dashboard')
def control_dashboard():

  return render_template("home/control_dashboard.html", title="Control")