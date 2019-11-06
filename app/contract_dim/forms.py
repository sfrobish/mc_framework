from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ContractForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Contract Name', validators=[DataRequired(message="Contract Name is required")])
  description = StringField('Description', validators=[DataRequired(message="Contract Description is required")])
  parent_id = IntegerField('Parent')
  score = SelectField("Similarity Score", coerce=int, validators=[NumberRange(
      min=1, max=100, message="Input must be between 1-100"), DataRequired(message="Input required")])
  submit = SubmitField('Submit')