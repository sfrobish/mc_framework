from flask import Blueprint

domain_dim = Blueprint('domain_dim', __name__)

from . import views