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


class usage_dim(basemodel):
  __tablename__ = "usage_dim"
  usage_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  usage_name = db.Column(db.String(60), unique=True, nullable=False)
  usage_descr = db.Column(db.String(200), unique=False, nullable=False)
  parent_usage_id = db.Column(db.Integer, unique=False, nullable=True)
  similarity_score = db.Column(db.Integer, unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.usage_name = kwargs.get("usage_name")
    self.usage_descr = kwargs.get("usage_descr")
    self.parent_usage_id = kwargs.get("parent_usage_id")
    self.similarity_score = kwargs.get("similarity_score")


class source_dim(basemodel):
  __tablename__ = "source_dim"
  source_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  source_name = db.Column(db.String(60), unique=True, nullable=False)
  source_descr = db.Column(db.String(200), unique=False, nullable=False)
  parent_source_id = db.Column(db.Integer, unique=True, nullable=True)
  similarity_score = db.Column(db.Integer, unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.source_descr = kwargs.get("source_descr")
    self.source_name = kwargs.get("source_name")
    self.parent_source_id = kwargs.get("parent_source_id")
    self.similarity_score = kwargs.get("similarity_score")


class geography_dim(basemodel):
  __tablename__ = "geography_dim"
  geo_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  geo_name = db.Column(db.String(60), unique=True, nullable=False)
  geo_descr = db.Column(db.String(200), unique=False, nullable=False)
  parent_geo_id = db.Column(db.Integer, unique=True, nullable=True)
  similarity_score = db.Column(db.Integer, unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.geo_name = kwargs.get("geo_name")
    self.geo_descr = kwargs.get("geo_descr")
    self.parent_geo_id = kwargs.get("parent_geo_id")
    self.similarity_score = kwargs.get("similarity_score")


class domain_dim(basemodel):
  __tablename__ = "domain_dim"
  domain_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  domain_name = db.Column(db.String(60), unique=True, nullable=False)
  domain_descr = db.Column(db.String(200), unique=False, nullable=False)
  parent_domain_id = db.Column(db.Integer, unique=False, nullable=True)
  similarity_score = db.Column(db.Integer, unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.domain_id = kwargs.get("domain_id")
    self.domain_name = kwargs.get("domain_name")
    self.domain_descr = kwargs.get("domain_descr")
    self.parent_domain_id = kwargs.get("parent_domain_id")
    self.similarity_score = kwargs.get("similarity_score")


class contract_dim(basemodel):
  __tablename__ = "contract_dim"
  contract_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  contract_name = db.Column(db.String(60), unique=True, nullable=False)
  contract_descr = db.Column(db.String(200), unique=False, nullable=False)
  parent_contract_id = db.Column(db.Integer, unique=False, nullable=True)
  similarity_score = db.Column(db.Integer, unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.contract_id = kwargs.get("contract_id")
    self.contract_name = kwargs.get("contract_name")
    self.contract_descr = kwargs.get("contract_descr")
    self.parent_contract_id = kwargs.get("parent_contract_id")
    self.similarity_score = kwargs.get("similarity_score")


class sdf_dim(basemodel):
  __tablename__ = "sensitive_data_fields"
  sdf_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  sdf_name = db.Column(db.String(60), unique=True, nullable=False)
  sdf_descr = db.Column(db.String(200), unique=False, nullable=False)
  sdf_regex = db.Column(db.String(200), unique=False, nullable=False)
  risk_score = db.Column(db.Integer, unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.sdf_id = kwargs.get("sdf_id")
    self.sdf_name = kwargs.get("sdf_name")
    self.sdf_descr = kwargs.get("sdf_descr")
    self.sdf_regex = kwargs.get("sdf_regex")
    self.risk_score = kwargs.get("risk_score")


class ident_dim(basemodel):
  __tablename__ = "identifiability_rules"
  rule_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  risk_type = db.Column(db.String(20), unique=False, nullable=False)
  risk_score = db.Column(db.Integer, unique=False, nullable=False)
  field_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False)

  def __init__(self, **kwargs):
    self.rule_id = kwargs.get("rule_id")
    self.risk_type = kwargs.get("risk_type")
    self.risk_score = kwargs.get("risk_score")
    self.field_list = kwargs.get("field_list")


class submitted_forms(basemodel):
  __tablename__ = "submitted_forms"
  submission_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  domain_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  source_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  geography_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  usage_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  rights_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  contract_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  identifiability_rule_id_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  #submitted_timestamp = db.Column(db.TIMESTAMP, unique=False, nullable=False, primary_key=False)

  def __init__(self, **kwargs):
    self.classification_id = kwargs.get("classification_id")
    self.domain_id_list = kwargs.get("domain_id_list")
    self.source_id_list = kwargs.get("source_id_list")
    self.geography_id_list = kwargs.get("geography_id_list")
    self.usage_id_list = kwargs.get("usage_id_list")
    self.rights_id_list = kwargs.get("rights_id_list")
    self.contract_id_list = kwargs.get("contract_id_list")
    self.identifiability_rule_id_list = kwargs.get("identifiability_rule_id_list")
    #self.submitted_timestamp = kwargs.get("submitted_timestamp")


class classification(basemodel):
  __tablename__ = "classification"
  classification_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  domain_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  source_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  geography_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  usage_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  rights_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  contract_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  identifiability_rule_list = db.Column(db.ARRAY(db.Integer), unique=False, nullable=False, primary_key=False)
  recipe_id = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
  label = db.Column(db.String(60), unique=False, nullable=False, primary_key=False)

  def __init__(self, **kwargs):
    self.classification_id = kwargs.get("classification_id")
    self.domain_list = kwargs.get("domain_list")
    self.source_list = kwargs.get("source_list")
    self.geography_list = kwargs.get("geography_list")
    self.usage_list = kwargs.get("usage_list")
    self.rights_list = kwargs.get("rights_list")
    self.contract_list = kwargs.get("contract_list")
    self.identifiability_rule_list = kwargs.get("identifiability_rule_list")
    self.recipe_id = kwargs.get("recipe_id")
    self.label = kwargs.get("label")
