from flask import Blueprint

contract = Blueprint('contract', __name__)

from . import views