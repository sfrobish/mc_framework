from flask import Blueprint

sdf_dim = Blueprint('sdf_dim', __name__)

from . import views