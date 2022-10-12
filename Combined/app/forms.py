from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddResearcherForm(FlaskForm):
    researcher = IntegerField('Scopus ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangeAPIKey(FlaskForm):
    APIKey = StringField('API Key', validators=[DataRequired()])
    submit = SubmitField('Submit')