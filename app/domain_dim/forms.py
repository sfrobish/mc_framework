from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired

class DomainForm(FlaskForm):

    #Form for admin to add or edit a domain
    name = SelectField("domain_dim", coerce=int)
    description = StringField('Description', coerce=str)
    submit = SubmitField('Submit')
    #will need to add more fields according to form