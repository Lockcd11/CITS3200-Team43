from flask import render_template, flash
from app import app
from app.forms import AddResearcherForm, ChangeAPIKey
from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval
from sortedcontainers import SortedSet
import pandas as pd
import csv

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/researchers.html', methods=['GET', 'POST'])
def researchers():
    form1 = AddResearcherForm()
    form2 = ChangeAPIKey()
    if form1.validate_on_submit():
        seniorFlag = form1.senior.data
        if seniorFlag is True:
            csvmaker(1, form1.researcher.data, 1)
        if seniorFlag is False:
            csvmaker(1, form1.researcher.data)
        flash('Researcher added', 'success')
        return render_template('researchers.html', form1=form1, form2=form2)
    if form2.validate_on_submit():
        pass
    return render_template('researchers.html', form1=form1, form2=form2)

@app.route('/tool.html')
def tool():
    return render_template('tool.html')

def csvmaker(mode, id, senior=0): # Accepts 0 for standard run, 1 for add, 2 for removal. if senior flag set to one, given senior researcher treatment
    if mode == 1:
        new_researcher=id
    else:
        new_researcher=None
    if mode ==2:
        researcher_for_removal=id
    else:
        researcher_for_removal=None
    if senior == 1:
        senior_flag=1
    else:
        senior_flag=0

    coreTeam=[]
    seniorTeam=[7402517928, 7201664962, 6603302385, 7102860769]
    if senior_flag==1:
        seniorTeam.append(id)
    with open('app/static/csvs/coreteam.csv', 'r', newline='') as csvfile:
        readin = csv.reader(csvfile)
        firstrow=0
        for row in readin:
            if firstrow==0:
                firstrow+=1
            else:
                coreTeam.append(row)
    if new_researcher != None:
        coreTeam.append([new_researcher])
    if researcher_for_removal != None:
        for each in coreTeam:
            if each[0]==researcher_for_removal:
                coreTeam.remove(each)

    with open('app/static/csvs/coreteam.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['scopus id'])
        for x in coreTeam:
            csv_out.writerow([str(x[0])])

    with open('app/static/csvs/seniorteam.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['scopus id'])
        for x in seniorTeam:
            csv_out.writerow([str(x)])
