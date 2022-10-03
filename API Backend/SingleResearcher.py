from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval
from sortedcontainers import SortedSet
from argparse import ArgumentParser
import pandas as pd
import csv
import argparse

targetedResearcher=None
researcherQueue = []
parser = argparse.ArgumentParser()
parser.add_argument("researcher", help="id of researcher")
parser.add_argument("depth", help="depth of researcher being checked")
parser.add_argument("--senior", help="if not None, opens up limits to account for increased co-authorship")
args=parser.parse_args()
researcherQueue.append(args.researcher)
targetedResearcher=args.researcher
newDepth=args.depth
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
    pubs_fullinfo.append([pubretrieval.identifier, pubretrieval.title, pubretrieval.subtype, pubretrieval.publisher, pubretrieval.scopus_link])
    thisPublicationAuthors = pd.DataFrame(pubretrieval.authors)
    if len(thisPublicationAuthors.iloc[:,0])<30:
        author=0
        for x in thisPublicationAuthors.iloc[:,0]:
            relationships.add((thisPublication, x))
            researchers_fullinfo.append([x, thisPublicationAuthors.iloc[:,3][author]+' '+thisPublicationAuthors.iloc[:,2][author],'https://www.scopus.com/authid/detail.uri?authorId='+str(x), newDepth+1])
            author+=1
with open(str(targetedResearcher)+' relationships.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['publication eid', 'author id'])
    for x in relationships:
        csv_out.writerow(x)
with open(str(targetedResearcher)+' researchers.csv', 'w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['researcher'])
    for x in researchers:
        csv_out.writerow([str(x)])
with open(str(targetedResearcher)+' publications.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['publication'])
    for x in publications:
        csv_out.writerow([x])
with open(str(targetedResearcher)+' fullresearchers.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['id', 'name', 'link', 'degrees'])
    for x in researchers_fullinfo:
        csv_out.writerow(x)
if len(researcherErrors)>0:
    with open(str(targetedResearcher)+' errors.csv', 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['id'])
        for x in researcherErrors:
            csv_out.writerow([x])