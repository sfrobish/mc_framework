from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class Source_DimForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Name', validators=[DataRequired(message="Name is required")])
  description = StringField('Description', validators=[DataRequired(message="Description is required")])
  parent_id = SelectField("Parent Id", coerce=int, validators=[DataRequired(message="Id is required")])
  score = SelectField("Score", coerce=int, validators=[DataRequired(message="Score is required")])
  submit = SubmitField('Submit')