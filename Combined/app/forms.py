from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class AddResearcherForm(FlaskForm):
    researcher = IntegerField('Scopus ID', validators=[DataRequired()])
    senior = BooleanField('Senior Researcher')
    submit = SubmitField('Submit')

class ChangeAPIKey(FlaskForm):
    APIKey = StringField('API Key', validators=[DataRequired()])
    submit = SubmitField('Submit')
