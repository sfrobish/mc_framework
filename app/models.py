#!/usr/bin/env python3

from app import db


class basemodel(db.Model):
  __abstract__ = True
  __table_args__ = {"schema":"mc_demo"}

#  def __init__(self, *args):
#    super().__init__(*args)

  def __repr__(self):
    # Define a base way to print models
    return '%s(%s)' % (self.__class__.__name__, {
      column: value
      for column, value in self._to_dict().items()
    })

  def json(self):
    # Define a base way to jsonify models, dealing with datetime objects
    return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
    }


class control(basemodel):
  __tablename__ = "control"
  control_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  control_name = db.Column(db.String(60), unique=True, nullable=False)
  control_description = db.Column(db.String(200), unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.control_description = kwargs.get("control_description")
    self.control_name = kwargs.get("control_name")


class recipe(basemodel):
  __tablename__ = "recipe"
  recipe_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  recipe_name = db.Column(db.String(60), unique=True, nullable=False)
  recipe_description = db.Column(db.String(200), unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.recipe_name = kwargs.get("recipe_name")
    self.recipe_description = kwargs.get("recipe_description")


class control_recipe(basemodel):
  __tablename__ = "control_recipe"
  control_recipe_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  recipe_id = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
  control_id = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)

  def __init__(self, **kwargs):
    self.recipe_id = kwargs.get("recipe_id")
    self.control_id = kwargs.get("control_id")


class classification(basemodel):
  __tablename__ = "classification"
  classification_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  classification_version = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  domain_id = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
  source_id = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
  usage_id = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
  geo_id = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
  rights_id = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
  data_elem_class_id = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
  control_recipe_id = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
  classification_label = db.Column(db.String(60), unique=False, nullable=False, primary_key=False)
  created_tstmp = db.Column(db.TIMESTAMP, nullable=False)

  def __init__(self, **kwargs):
    self.classification_id = kwargs.get("classification_id")
    self.domain_id = kwargs.get("domain_id")
    self.source_id = kwargs.get("source_id")
    self.usage_id = kwargs.get("usage_id")
    self.geo_id = kwargs.get("geo_id")
    self.rights_id = kwargs.get("rights_id")
    self.control_recipe_id = kwargs.get("control_recipe_id")
    self.classification_label = kwargs.get("classification_label")
