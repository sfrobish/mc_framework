from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from . import home

@home.route('/', methods=['GET', 'POST'])
def homepage():
  if current_user.is_authenticated:
    # Render the homepage template on the / route
    return render_template('home/index.html', current_user=current_user, title="Welcome")
  else:
    return redirect(url_for('auth.login'))


@home.route('/control/dashboard')
@login_required
def control_dashboard():

  return render_template("home/control_dashboard.html", title="Control")
