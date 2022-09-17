from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval
from sortedcontainers import SortedSet
import pandas as pd
import csv

depth=0
coreTeam = [57219019970, 57216501896, 57210644282, 57209335346, 57208166414, 57221013971, 57203278857, 57195488227, 57004266000, 56306019600, 55659418600, 53263517200, 36641521800, 35409967700, 7402517928,7401755590, 7201664962, 7102860769, 7003410036, 6603302385, 6603217918, 6602103486]

researcherQueue = []
publicationQueue = []
researchers = SortedSet()
publications = SortedSet()
relationships = SortedSet()
names=0

for x in coreTeam:
    researcherQueue.append(x)
while depth < 2:
    while len(researcherQueue)!=0:
        print(len(researcherQueue))
        thisResearcher=researcherQueue[0]
        researcherQueue.pop(0)
        researcherFile = AuthorRetrieval(thisResearcher)
        print(researcherFile.get_key_reset_time())
        thisAuthorPublications = pd.DataFrame(researcherFile.get_document_eids())
        for x in thisAuthorPublications[0]:
            if x not in publications:
                publicationQueue.append(x)
            publications.add(x)
    print(len(publications))
    while len(publicationQueue)!=0:
        thisPublication=publicationQueue[0]
        publicationQueue.pop(0)
        thisPublicationAuthors = None
        thisPublicationAuthors = pd.DataFrame(AbstractRetrieval(thisPublication).authors)
        if len(thisPublicationAuthors.iloc[:,0])<50:
            for x in thisPublicationAuthors.iloc[:,0]:
                relationships.add((thisPublication, x))
                if depth !=2:
                    if x not in researchers:
                        researcherQueue.append(x)
                    researchers.add(x)
    depth=depth+1
    print('depthup')
with open('relationships.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['publication eid', 'author id'])
    for x in relationships:
        csv_out.writerow(x)
with open('researchers.csv', 'w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['researcher'])
    for x in researchers:
        csv_out.writerow([str(x)])
with open('publications.csv', 'w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['publication'])
    for x in publications:
        csv_out.writerow([x])
