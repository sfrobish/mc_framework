from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Source_DimForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Name', validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired()])
  submit = SubmitField('Submit')