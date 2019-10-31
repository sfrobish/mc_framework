from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class GeographyForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Name', validators=[
                     DataRequired(message="Name is invalid")])
  description = StringField('Description', validators=[
                            DataRequired(message="Description is invalid")])
  parent = IntegerField('Parent')
  similarity = IntegerField('Similarity Score', validators=[NumberRange(
      min=1, max=100, message="Input must be between 1-100"), DataRequired(message="Input required")])
  submit = SubmitField('Submit')