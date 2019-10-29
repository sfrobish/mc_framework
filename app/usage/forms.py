from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UsageForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Name', validators=[DataRequired(message="Name is invalid")])
  description = StringField('Description', validators=[DataRequired(message="Description is invalid")])
  submit = SubmitField('Submit')