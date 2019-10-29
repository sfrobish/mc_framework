import os

class Config(object):

    # Put any configurations here that are common across all environments
   SQLALCHEMY_TRACK_MODIFICATIONS = False # silence the deprecation warning


class DevelopmentConfig(Config):
    
  # Development configurations

  DEBUG = True
  SQLALCHEMY_ECHO = True

  DB_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/mc_demo'
  SQLALCHEMY_DATABASE_URI = DB_URL 

  SECRET_KEY = os.urandom(32)


class ProductionConfig(Config):

  # Production configurations

  DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}