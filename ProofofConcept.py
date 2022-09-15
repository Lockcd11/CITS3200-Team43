from pybliometrics.scopus.utils import config
from pybliometrics.scopus import AuthorSearch
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval
import pandas as pd


CoreResearcher = AuthorRetrieval(36641521800) #retrieve Dr Ward
publications = pd.DataFrame(CoreResearcher.get_document_eids()) #retrieve all publications by Dr Ward
pubEids = [] #array of eIDs of Dr Ward's publications
for x in publications[0]: #For each publication of dr ward
    if x not in pubEids: #If we haven't already checked it
        pubEids.append(x) #Add it to the list
abstract = AbstractRetrieval(pubEids[0]) #for the first of Dr Ward's publications
auidList = pd.DataFrame(abstract.authors) #Get it's info
firstdeg = [] #Initialise list of first degree contacts
for x in auidList[0]: #For each contact
    if x not in firstdeg: #If they're not already in our lists
        firstdeg.append(x) #Add them to the list

#s = AuthorSearch('AU-ID(36641521800)')
#print(s)
#print(s.authors[0])