from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class Source_DimForm(FlaskForm):

  # Form for admin to add or edit a department
  name = StringField('Name', validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired()])
  parent_id = SelectField("Parent Id", coerce=int)
  score = SelectField("Score", coerce=int)
  submit = SubmitField('Submit')