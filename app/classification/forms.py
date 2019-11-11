from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList
from wtforms.validators import DataRequired


class ClassificationForm(FlaskForm):
  
  domain_list = FieldList(IntegerField("domain"))
  source_list = FieldList(IntegerField("source"))
  geography_list = FieldList(IntegerField("geography"))
  usage_list = FieldList(IntegerField("usage"))
  rights_list = FieldList(IntegerField("rights"))
  contract_list = FieldList(IntegerField("contract"))
  fields_string = StringField("sensitive_fields_list")
  recipe_id = IntegerField("recipe_id")
  label = StringField("label", validators=[DataRequired(message="Classification Label is required")])
  submit = SubmitField('Submit')