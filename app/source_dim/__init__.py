from flask import Blueprint

source_dim = Blueprint('source_dim', __name__)

from . import views