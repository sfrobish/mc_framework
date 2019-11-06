from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SensitiveFieldsForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField("Name", validators=[DataRequired(message="Name is required")])
  description = StringField("Description", validators=[DataRequired(message="Description is required")])
  regex = StringField("Regular Expression", validators=[DataRequired(message="Regex is required")])
  score = SelectField("Sensitivity Score", coerce=int, validators=[DataRequired(message="Score is required")])
  submit = SubmitField("Submit")