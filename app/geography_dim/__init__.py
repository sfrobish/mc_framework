from flask import Blueprint

geography = Blueprint('geography', __name__)

from . import views