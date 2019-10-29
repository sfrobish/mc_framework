from flask import Blueprint

control_recipe = Blueprint('control_recipe', __name__)

from . import views