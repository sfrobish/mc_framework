from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange

class DomainForm(FlaskForm):

  #Form for admin to add or edit a domain
  name = StringField('Name', validators=[DataRequired(message="Name is invalid")])
  description = StringField('Description', validators=[DataRequired(message="Description is invalid")])
  parent = IntegerField('Parent')
  similarity = IntegerField('Similarity Score', validators=[NumberRange(
      min=1, max=100, message="Input must be between 1-100"), DataRequired(message="Input required")])
  submit = SubmitField('Submit')
    