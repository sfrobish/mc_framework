from flask import Blueprint
from ..helpers import check_admin
from flask_login import login_required

control = Blueprint('control', __name__)

from . import views
