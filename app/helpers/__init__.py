from flask import abort
from flask_login import current_user

def check_admin():
  # prevent non-admins from accessing the page
  if not current_user.user_is_admin:
    abort(403)
