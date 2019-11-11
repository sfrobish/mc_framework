from flask import Blueprint

ident_dim = Blueprint('ident_dim', __name__)

from . import views