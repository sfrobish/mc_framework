from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired


class RecipeForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Name', validators=[DataRequired(DataRequired(message="Name is invalid"))])
  description = StringField('Description', validators=[DataRequired(message="Description is invalid")])
  submit = SubmitField('Submit')
