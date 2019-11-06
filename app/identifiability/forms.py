from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class IdentifiabilityForm(FlaskForm):

  # Form for admin to add or edit a department
  is_pii = BooleanField("IsPII", validators=[DataRequired(message="IsPII flag is required")])
  risk_score = SelectField("Risk Score", coerce=int, validators=[DataRequired(message="Score is required")])
  field_list = StringField("Description", validators=[DataRequired(message="Field List is required")])
  submit = SubmitField("Submit")