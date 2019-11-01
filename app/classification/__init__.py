from flask import Blueprint

classification = Blueprint('classification', __name__)

from . import views