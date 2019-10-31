from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class UsageForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Name', validators=[DataRequired(message="Name is invalid")])
  description = StringField('Description', validators=[DataRequired(message="Description is invalid")])
  parent_id = SelectField("Parent Id", coerce=int, validators=[DataRequired(message="Parent is invalid")])
  score = SelectField("Score", coerce=int, validators=[DataRequired(message="Score is invalid")])
  submit = SubmitField('Submit')