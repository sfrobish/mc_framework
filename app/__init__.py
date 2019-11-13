#!/usr/bin/env python3


from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

# local imports
from config import app_config

from app.extensions import csrf


# db variable initialization
db = SQLAlchemy()

def create_app(config_name):

  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object(app_config[config_name])
  #app.config.from_pyfile('config.py')

  # setup for flask_login
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  from .models import user

  @login_manager.user_loader
  def load_user(user_id):
    return user.query.get(int(user_id))

  def role_required(role_name):
    def decorator(func):
      @wraps(func)
      def authorize(*args, **kwargs):
        if not current_user.has_role(role_name):
          abort(401) # not authorized
        return func(*args, **kwargs)
      return authorize
    return decorator

  Bootstrap(app)
  csrf.init_app(app)
  db.init_app(app)

  migrate = Migrate(app, db)
  from app import models

  # blueprint for auth routes in our app
  from .auth import auth as auth_blueprint
  csrf.exempt(auth_blueprint)
  app.register_blueprint(auth_blueprint)

  from .home import home as home_blueprint
  app.register_blueprint(home_blueprint)

  from .control import control as control_blueprint
  csrf.exempt(control_blueprint)
  app.register_blueprint(control_blueprint)

  from .recipe import recipe as recipe_blueprint
  csrf.exempt(recipe_blueprint)
  app.register_blueprint(recipe_blueprint)
  
  from .control_recipe import control_recipe as control_recipe_blueprint
  app.register_blueprint(control_recipe_blueprint)
  
  from .domain_dim import domain as domain_blueprint
  app.register_blueprint(domain_blueprint)
  
  from .geography_dim import geography as geography_blueprint
  csrf.exempt(geography_blueprint)
  app.register_blueprint(geography_blueprint)

  from .source_dim import source_dim as source_blueprint
  csrf.exempt(source_blueprint)
  app.register_blueprint(source_blueprint)

  from .usage_dim import usage as usage_blueprint
  csrf.exempt(usage_blueprint)
  app.register_blueprint(usage_blueprint)

  from .contract_dim import contract as contract_blueprint
  csrf.exempt(contract_blueprint)
  app.register_blueprint(contract_blueprint)

  from .sensitive_fields import sdf_dim as sdf_blueprint
  csrf.exempt(sdf_blueprint)
  app.register_blueprint(sdf_blueprint)

  from .identifiability import ident_dim as ident_blueprint
  csrf.exempt(ident_blueprint)
  app.register_blueprint(ident_blueprint)  

  from .classification import classification as classification_blueprint
  csrf.exempt(classification_blueprint)
  app.register_blueprint(classification_blueprint)


  return app
