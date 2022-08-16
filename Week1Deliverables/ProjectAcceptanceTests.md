**Things that need to be tested:**	How to test them
- **Initial setup on different devices with a set list of researches:** 	Start the program on multiple devices to see if setup is consistent
- **Load after setup:**	Once initial setup has been completed, run the program again and make sure timestamp of last updated has changed and if things need to be updated                         since last timestamp it'll update database correctly.
- **Add/remove researcher:** Add/remove a researcher using the web app and see if the list is updated
- **Update database after adding/removing a researcher:**	Once a researcher has been added/removed see if the database has been updated correctly
- **Search engine:**	To search for a specific research team member and get all other researches information that they have worked with.
- **Graph of data:**	Once you have used the search engine, you'll need to see if the graph option displays all information in a readable manner 
	
	
	
	
Extra ideas???

**Things that need to be tested:**	How to test them
- **A time update log:**	On the home page of the app, it'll have a display of all updated documents (if none is found, it'll say "No newest update" or something like                             that. And we can test for this by manually setting the timestamp to before an update was made, then updating it to make sure said data changes                           appear


Todo:
Match acceptance tests to Dr Wards value attributes.
Weighted for totals,:
$25 for Core two degrees of separation
$20 for visualising further degrees of separation
$10 for requesting further information on specific individuals
$20 for adding and removing members of the core team
$15 for filtering by specific researchers and publications
$10 for filtering by specific topics

Add tests for;
Query API and store results into database

Under how to test add stuff that confirms the program is doing what we want it to do;
for example for the graph add a test that checks if two researchers are being displayed as proper links,
add test to see if Query responds with expected researcher from SCOPUS ID
add test for seeing if database for core researchers changes when you want it to

