from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval
import pandas as pd

depth=0
coreTeam = list()
researcherQueue = []
researcherQueue.append(36641521800)
researcherQueue.append(6602103486)
publicationQueue = []
researchers = {
}

publications = {
}

for x in coreTeam:
    researcherQueue.append(coreTeam[x])

while len(researcherQueue)!=0:
    thisResearcher=researcherQueue[0]
    researcherQueue.pop(0)
    if thisResearcher not in researchers.keys():
        researchers.update({thisResearcher:set()})
        researcherFile = AuthorRetrieval(thisResearcher)
        thisAuthorPublications = pd.DataFrame(researcherFile.get_document_eids())
        for x in thisAuthorPublications[0]:
            researchers[thisResearcher].add(x)
            if x not in publications.keys():
                publicationQueue.append(x)
                publications.update({x:set()})
            publications[x]=(publications.get(x).add(thisResearcher))
    
while len(publicationQueue)!=0:
    thisPublication=publicationQueue[0]
    publicationQueue.pop(0)
    thisPublicationAuthors = pd.DataFrame(AbstractRetrieval(thisPublication).authors)
    for x in thisPublicationAuthors.iloc[:,0]:
        if publications.get(thisPublication)==None:
            publications.update({thisPublication:set()})
        publications[thisPublication].add(x)
        if (x not in researchers.keys()) or (researchers.get(x)==None):
            researcherQueue.append(x)
            researchers.update({x:set()})
            researchers[x].add(thisPublication)
        researchers[x]=(researchers.get(x).add(thisPublication))

print("Researchers", researchers)
print("Publications", publications)




    

# CoreResearcher = AuthorRetrieval(36641521800) #retrieve Dr Ward
# publications = pd.DataFrame(CoreResearcher.get_document_eids()) #retrieve all publications by Dr Ward
# pubEids = [] #array of eIDs of Dr Ward's publications
# for x in publications[0]: #For each publication of dr ward
#     if x not in pubEids: #If we haven't already checked it
#         pubEids.append(x) #Add it to the list
# abstract = AbstractRetrieval(pubEids[0]) #for the first of Dr Ward's publications
# auidList = pd.DataFrame(abstract.authors) #Get it's info
# firstdeg = [] #Initialise list of first degree contacts
# for x in auidList[0]: #For each contact
#     if x not in firstdeg: #If they're not already in our lists
#         firstdeg.append(x) #Add them to the list

# #s = AuthorSearch('AU-ID(36641521800)')
# #print(s)
# #print(s.authors[0])