from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired

class AddResearcherForm(FlaskForm):
    researcher = IntegerField('Scopus ID', validators=[DataRequired()])
    addremoveupdate = RadioField('Add / Remove / Update', choices=[('Add','Add Researcher'),('Remove','Remove Researcher'),('Update', 'Update Researcher')])
    senior = BooleanField('Senior Researcher')
    submit = SubmitField('Submit')

class ChangeAPIKey(FlaskForm):
    APIKey = StringField('API Key', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ExpandForm(FlaskForm):
    researcher = IntegerField('Scopus Id', validators=[DataRequired()])
    submit = SubmitField('Expand')
