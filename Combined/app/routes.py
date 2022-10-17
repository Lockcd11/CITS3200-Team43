from flask import render_template, flash
from app import app
from app.forms import AddResearcherForm, ChangeAPIKey, ExpandForm
from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval
from sortedcontainers import SortedSet
import pandas as pd
import csv
import os
from app.static.pythonScripts.inisial import create_db
from app.static.pythonScripts.update import update_db

os.environ['PYB_CONFIG_FILE'] = "./pyconfig.ini"

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
        modeFlag = form1.addremoveupdate.data
        if modeFlag == 'Add':
            modeInput = 1
        if modeFlag == 'Remove':
            modeInput = 2
        if modeFlag == 'Update':
            modeInput = 0
        if seniorFlag is True and modeInput is not None:
            csveditor(modeInput, form1.researcher.data, 1)
        if seniorFlag is False and modeInput is not None:
            csveditor(modeInput, form1.researcher.data)
        if seniorFlag is 1:
            csvmaker(1)
        else:
            csvmaker()
        create_db()
        flash('Researcher added', 'success')
        return render_template('researchers.html', form1=form1, form2=form2)
    if form2.validate_on_submit():
        f = open("./pyconfig.ini", "w")
        f.write("[Directories]\nAbstractRetrieval = ./.pybliometrics/Scopus/abstract_retrieval\nAffiliationRetrieval = ./.pybliometrics/Scopus/affiliation_retrieval\nAffiliationSearch = ./.pybliometrics/Scopus/affiliation_search\nAuthorRetrieval = ./.pybliometrics/Scopus/author_retrieval\nAuthorSearch = ./.pybliometrics/Scopus/author_search\nCitationOverview = ./.pybliometrics/Scopus/citation_overview\nScopusSearch = ./.pybliometrics/Scopus/scopus_search\nSerialSearch = ./.pybliometrics/Scopus/serial_search\nSerialTitle = ./.pybliometrics/Scopus/serial_title\nPlumXMetrics = ./.pybliometrics/Scopus/plumx\nSubjectClassifications = ./.pybliometrics/Scopus/subject_classification\n\n[Authentication]\nAPIKey = " + form2.APIKey.data + "\n\n[Requests]\nTimeout = 20") #EDIT TO FIT WHERE THE ACTUAL FILES WILL GO
        f.close()
        flash('API Key Changed', 'success')
        return render_template('researchers.html', form1=form1, form2=form2)

    return render_template('researchers.html', form1=form1, form2=form2)

@app.route('/tool.html')
def tool():
    form1 = ExpandForm()
    if form1.validate_on_submit():
        expand(form1.researcher.data)
        update_db()
    return render_template('tool.html', form1=form1)

def csveditor(mode, id, senior=0): # Accepts 0 for update, 1 for add, 2 for removal. if senior flag set to one, given senior researcher treatment
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
    if mode == 0:
        update_researcher=id
    else:
        update_researcher=None

    coreTeam=[]
    seniorTeam=[]
    if mode != 0:
        if senior_flag == 0:
            with open('app/static/pythonScripts/current_csvs/coreteam.csv', 'r', newline='') as csvfile:
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
        if senior_flag == 1:
            with open('app/static/pythonScripts/current_csvs/seniorteam.csv', 'r', newline='') as csvfile:
                readin = csv.reader(csvfile)
                firstrow=0
                for row in readin:
                    if firstrow==0:
                        firstrow+=1
                    else:
                        seniorTeam.append(row)
            if new_researcher != None:
                seniorTeam.append([new_researcher])
            if researcher_for_removal != None:
                for each in seniorTeam:
                    if each[0]==researcher_for_removal:
                        seniorTeam.remove(each)
    if mode == 0:
        with open('app/static/PythonScripts/current_csvs/updates.csv', 'w', newline='') as csvfile:
            readin = csv.reader(csvfile)
            writeout = csv.writer(csvfile)
            for x in readin:
                depth = x[4]
                if x[0]==update_researcher:
                    researcherFile = AuthorRetrieval(readin[0], True)
                    data = [researcherFile.identifier, researcherFile.given_name+' '+researcherFile.surname, 'https://www.scopus.com/authid/detail.uri?authorId='+str(researcherFile.identifier),researcherFile.coauthor_count, depth]
                else:
                    data = x
                writeout.writerow(data)

    

    with open('app/static/pythonScripts/current_csvs/coreteam.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['scopus id'])
        for x in coreTeam:
            csv_out.writerow([str(x[0])])

    with open('app/static/pythonScripts/current_csvs/seniorteam.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['scopus id'])
        for x in seniorTeam:
            csv_out.writerow([str(x)])

def csvmaker(senior=0):
    coreTeam=[]
    seniorTeam=[7402517928, 7201664962, 6603302385, 7102860769]
    with open('app/static/pythonScripts/current_csvs/coreteam.csv', 'r', newline='') as csvfile:
        readin = csv.reader(csvfile)
        firstrow=0
        for row in readin:
            if firstrow==0:
                firstrow+=1
            else:
                coreTeam.append(row)
    researcherErrors=[]
    with open('app/static/pythonScripts/current_csvs/seniorteam.csv', 'r', newline='') as csvfile:
        readin = csv.reader(csvfile)
        firstrow=0
        for row in readin:
            if firstrow==0:
                firstrow+=1
            else:
                seniorTeam.append(row)
    
    researcherQueue = []
    publicationQueue = []
    researchers = SortedSet()
    researchers_fullinfo = []
    publications = SortedSet()
    pubs_fullinfo = []
    relationships = SortedSet()
    for x in seniorTeam
        researcherQueue.append(x)
    depth=4
    while len(researcherQueue)!=0:
            print(len(researcherQueue))
            thisResearcher=researcherQueue[0]
            researcherQueue.pop(0)
            try:
                researcherFile = AuthorRetrieval(thisResearcher)
                researchers_fullinfo.append([researcherFile.identifier, researcherFile.given_name+' '+researcherFile.surname, 'https://www.scopus.com/authid/detail.uri?authorId='+str(researcherFile.identifier),researcherFile.coauthor_count, depth])     
                researchers.add(researcherFile.identifier)
                thisAuthorPublications = pd.DataFrame(researcherFile.get_document_eids())
                if researcherFile.coauthor_count < 250:
                    for x in thisAuthorPublications[0]:
                        if x not in publications:
                            publicationQueue.append(x)
                        publications.add(x)
                else:
                    publications.add(x)
                    relationships.add(x, researcherFile.identifier)
            except:
                researcherErrors.append(str(thisResearcher))
                for each in coreTeam:
                    if each[0]==thisResearcher:
                        coreTeam.remove(each)
        while len(publicationQueue)!=0:
            thisPublication=publicationQueue[0]
            publicationQueue.pop(0)
            print(len(publicationQueue))
            pubretrieval=AbstractRetrieval(thisPublication)
            thisPublicationAuthors = pd.DataFrame(pubretrieval.authors)
            pubs_fullinfo.append([pubretrieval.identifier, pubretrieval.title, len(thisPublicationAuthors.iloc[:,0]), ("none" if pubretrieval.subtypedescription is None else pubretrieval.subtypedescription), ("none" if pubretrieval.publisher is None else pubretrieval.publisher), pubretrieval.scopus_link])
            if len(thisPublicationAuthors.iloc[:,0])<24:
                author=0
                for x in thisPublicationAuthors.iloc[:,0]:
                    relationships.add((pubretrieval.identifier, x))
                    if depth==4 and x not in researchers:
                        if x not in coreTeam:
                            try:
                                researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x),len(thisPublicationAuthors)-1 ,depth-2])
                            except:
                                researcherErrors.append(x)
                    if x not in researchers:
                        researcherQueue.append(x)
                    researchers.add(x)
                    author+=1
            else:
                author=0
                for x in thisPublicationAuthors.iloc[:,0]:
                    relationships.add((pubretrieval.identifier, x))
                    if depth==4 and x not in researchers:
                        if x not in coreTeam:
                            try:
                                researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x),len(thisPublicationAuthors)-1 ,depth-1])
                            except:
                                researcherErrors.append(x)
                    author+=1
    for x in coreTeam:
        researcherQueue.append(x[0])    
    depth=3
    while depth > 1:
        while len(researcherQueue)!=0:
            print(len(researcherQueue))
            thisResearcher=researcherQueue[0]
            researcherQueue.pop(0)
            try:
                researcherFile = AuthorRetrieval(thisResearcher)
                researchers_fullinfo.append([researcherFile.identifier, researcherFile.given_name+' '+researcherFile.surname, 'https://www.scopus.com/authid/detail.uri?authorId='+str(researcherFile.identifier),researcherFile.coauthor_count, depth])     
                researchers.add(researcherFile.identifier)
                thisAuthorPublications = pd.DataFrame(researcherFile.get_document_eids())
                if researcherFile.coauthor_count < 250:
                    for x in thisAuthorPublications[0]:
                        if x not in publications:
                            publicationQueue.append(x)
                        publications.add(x)
                else:
                    publications.add(x)
                    relationships.add(x, researcherFile.identifier)
            except:
                researcherErrors.append(str(thisResearcher))
                for each in coreTeam:
                    if each[0]==thisResearcher:
                        coreTeam.remove(each)
        while len(publicationQueue)!=0:
            thisPublication=publicationQueue[0]
            publicationQueue.pop(0)
            print(len(publicationQueue))
            pubretrieval=AbstractRetrieval(thisPublication)
            thisPublicationAuthors = pd.DataFrame(pubretrieval.authors)
            pubs_fullinfo.append([pubretrieval.identifier, pubretrieval.title, len(thisPublicationAuthors.iloc[:,0]), ("none" if pubretrieval.subtypedescription is None else pubretrieval.subtypedescription), ("none" if pubretrieval.publisher is None else pubretrieval.publisher), pubretrieval.scopus_link])
            if len(thisPublicationAuthors.iloc[:,0])<24:
                author=0
                for x in thisPublicationAuthors.iloc[:,0]:
                    relationships.add((pubretrieval.identifier, x))
                    if depth==2 and x not in researchers:
                        try:
                            researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x),len(thisPublicationAuthors)-1 ,depth-1])
                        except:
                            researcherErrors.append(x)
                    if x not in researchers:
                        researcherQueue.append(x)
                    researchers.add(x)
                    author+=1
            else:
                author=0
                for x in thisPublicationAuthors.iloc[:,0]:
                    relationships.add((pubretrieval.identifier, x))
                    if depth==2 and x not in researchers:
                        try:
                            researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x),len(thisPublicationAuthors)-1 ,depth-1])
                        except:
                            researcherErrors.append(x)
                    author+=1
        depth=depth-1
        print('depthup')
    with open('relationships.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['publication_eid', 'author_id'])
        for x in relationships:
            csv_out.writerow(x)
    with open('app/static/pythonScripts/current_csvs/researchers.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['id', 'name', 'link', 'coauthor_count' ,'degrees'])
        for x in researchers_fullinfo:
            csv_out.writerow(x)
    with open('app/static/pythonScripts/current_csvs/publications.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['id', 'title', 'author_count', 'type', 'publisher', 'link'])
        for x in pubs_fullinfo:
            csv_out.writerow(x)
    if len(researcherErrors)>0:
        with open('app/static/pythonScripts/current_csvs/errors.csv', 'w', newline='') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['id'])
            for x in researcherErrors:
                csv_out.writerow([x])
    with open('app/static/pythonScripts/current_csvs/coreteam.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['scopus id'])
        for x in coreTeam:
            csv_out.writerow([str(x[0])])

    return

def expand(researcher):
    targetedResearcher=researcher
    researcherQueue = []
    researcherQueue.append(researcher)
    newDepth=0
    publicationQueue = []
    researchers = SortedSet()
    researchers_fullinfo = []
    publications = SortedSet()
    relationships = SortedSet()
    pubs_fullinfo = []
    researchers_fullinfo = []
    researcherErrors=[]
    while len(researcherQueue)!=0:
        print(len(researcherQueue))
        thisResearcher=researcherQueue[0]
        researcherQueue.pop(0)
        try:
            researcherFile = AuthorRetrieval(thisResearcher)     
            thisAuthorPublications = pd.DataFrame(researcherFile.get_document_eids())
            for x in thisAuthorPublications[0]:
                if x not in publications:
                    publicationQueue.append(x)
                publications.add(x)
        except:
            researcherErrors.append(str(thisResearcher))
    while len(publicationQueue)!=0:
        thisPublication=publicationQueue[0]
        publicationQueue.pop(0)
        print(len(publicationQueue))
        pubretrieval=AbstractRetrieval(thisPublication)
        pubs_fullinfo.append([pubretrieval.identifier, pubretrieval.title, ("none" if pubretrieval.subtypedescription is None else pubretrieval.subtypedescription), ("none" if pubretrieval.publisher is None else pubretrieval.publisher), pubretrieval.scopus_link])
        thisPublicationAuthors = pd.DataFrame(pubretrieval.authors)
        if len(thisPublicationAuthors.iloc[:,0])<30:
            author=0
            for x in thisPublicationAuthors.iloc[:,0]:
                relationships.add((thisPublication, x))
                researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x), newDepth-1])
                author+=1
    with open('app/static/pythonScripts/current_csvs/add/relationships.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['publication eid', 'author id'])
        for x in relationships:
            csv_out.writerow(x)
    with open('app/static/pythonScripts/current_csvs/add/publications.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['id', 'title', 'author_count', 'type', 'publisher', 'link'])
        for x in publications:
            csv_out.writerow([x])
    with open('app/static/pythonScripts/current_csvs/add/fullresearchers.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['id', 'name', 'link', 'coauthor_count' ,'degrees'])
        for x in researchers_fullinfo:
            csv_out.writerow(x)
    return
