from flask import render_template, flash
from app import app
from app.forms import AddResearcherForm, ChangeAPIKey
from app.pyapi import DataStructure, SingleResearcher

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/researchers.html', methods=['GET', 'POST'])
def researchers():
    form1 = AddResearcherForm()
    if form1.validate_on_submit():
        flash('adding researcher', 'error')
        return('/researchers.html')
        # DataStructure("--add", form1.researcher)
        # flash('Researcher added', category="success")
        # return('/researchers.html')
        # add these back in once we know the form is working
    form2 = ChangeAPIKey()
    if form2.validate_on_submit():
        pass
    return render_template('researchers.html', form1=form1, form2=form2)

@app.route('/tool.html')
def tool():
    return render_template('tool.html')
