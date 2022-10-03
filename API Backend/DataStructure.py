from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval
from sortedcontainers import SortedSet
from argparse import ArgumentParser
import pandas as pd
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--add", help="adds researcher to core team")
parser.add_argument("--remove", help="removes researcher from core team")
parser.add_argument("--senior", help="adds one degree of senior researcher data")
args = parser.parse_args()
if args.add:
    new_researcher=args.add
else:
    new_researcher=None
if args.remove:
    researcher_for_removal=args.remove
else:
    researcher_for_removal=None
if args.senior:
    senior_flag=1
else:
    senior_flag=0

coreTeam=[]
seniorTeam=[7402517928, 7201664962, 6603302385, 7102860769]
with open('coreteam.csv', 'r', newline='') as csvfile:
    readin = csv.reader(csvfile)
    firstrow=0
    for row in readin:
        if firstrow==0:
            firstrow+=1
        else:
            coreTeam.append(row)
researcherErrors=[]
print(coreTeam)

depth=0
#coreTeam = [57219019970, 57216501896, 57210644282, 57209335346, 57208166414, 57221013971, 57203278857, 57195488227, 57004266000, 56306019600, 55659418600, 53263517200, 36641521800, 35409967700, 7402517928,7401755590, 7201664962, 7102860769, 7003410036, 6603302385, 6603217918, 6602103486]
#print(coreTeam)
if new_researcher != None:
    coreTeam.append([new_researcher])
if researcher_for_removal != None:
    for each in coreTeam:
        if each[0]==researcher_for_removal:
            coreTeam.remove(each)
researcherQueue = []
publicationQueue = []
researchers = SortedSet()
researchers_fullinfo = []
publications = SortedSet()
pubs_fullinfo = []
relationships = SortedSet()
names=0
for x in coreTeam:
    researcherQueue.append(x[0])
while depth < 2:
    while len(researcherQueue)!=0:
        print(len(researcherQueue))
        thisResearcher=researcherQueue[0]
        researcherQueue.pop(0)
        try:
            researcherFile = AuthorRetrieval(thisResearcher)
            researchers_fullinfo.append([researcherFile.identifier, researcherFile.given_name+' '+researcherFile.surname, 'https://www.scopus.com/authid/detail.uri?authorId='+str(researcherFile.identifier),researcherFile.coauthor_count, depth])     
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
        pubs_fullinfo.append([pubretrieval.identifier, pubretrieval.title, len(thisPublicationAuthors.iloc[:,0]), pubretrieval.subtypedescription, pubretrieval.publisher, pubretrieval.scopus_link])
        if len(thisPublicationAuthors.iloc[:,0])<25:
            author=0
            for x in thisPublicationAuthors.iloc[:,0]:
                relationships.add((pubretrieval.identifier, x))
                if depth==1 and x not in researchers:
                    try:
                        researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x),None ,depth+1])
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
                if depth==1 and x not in researchers:
                    try:
                        researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x),None ,depth+1])
                    except:
                        researcherErrors.append(x)
                author+=1
    depth=depth+1
    print('depthup')
with open('relationships.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['publication_eid', 'author_id'])
    for x in relationships:
        csv_out.writerow(x)
# with open('researchers.csv', 'w') as out: #Deprecated, was for printing just the researcher ids into a csv for testing
#     csv_out=csv.writer(out)
#     csv_out.writerow(['researcher'])
#     for x in researchers:
#         csv_out.writerow([str(x)])
# with open('publications.csv', 'w', newline='') as out: #Deprecated as above, but stored publication ids
#     csv_out=csv.writer(out)
#     csv_out.writerow(['publication'])
#     for x in publications:
#         csv_out.writerow([x])
with open('researchers.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['id', 'name', 'link', 'coauthor_count' ,'degrees'])
    for x in researchers_fullinfo:
        csv_out.writerow(x)
with open('publications.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['id', 'title', 'author_count', 'type', 'publisher', 'link'])
    for x in pubs_fullinfo:
        csv_out.writerow(x)
if len(researcherErrors)>0:
    with open('errors.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['id'])
        for x in researcherErrors:
            csv_out.writerow([x])
with open('coreteam.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['scopus id'])
    for x in coreTeam:
        csv_out.writerow([str(x[0])])
