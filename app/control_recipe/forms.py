from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class ControlRecipeForm(FlaskForm):

  # Form for admin to add or edit a department
  control = SelectField("Control", coerce=int)
  recipe = SelectField("Recipe", coerce=int)
  submit = SubmitField("Submit")