# Reqirement Analysis Document

# CITS3200 Team 43

## Semester 2 2022

### 1.0 General Goals
We would like to support researchers from our Centre of Research Excellence who are associated with different universities, institutes and health providers to see their extended research network and use this information to expand their collaborative reach.

We will primarily be focussing on the core research team of our client, Dr Tanya Ward.


### 2.0 Current System
For researchers, collaboration is critical to success. Yet siloes of people and information are still common. While researchers associated with universities may be able to access network maps associated with that institution, this is usually based on internal data that does not extend beyond the immediate links already in place for that person.

Our Client, Dr Tanya Ward, has provided us with the current system, which is simply a number of excel spreadsheets containing lists of papers and their contributors. Dr Ward also has access to databases with all of this information, but these databases are search-based, and do not natively allow for visual understanding, or assist in finding new potential collaborators.

### 3.0 Proposed System
#### 3.1 Overview
Our proposed system is a network mapping visualiser, a visual tool to demonstrate connection and reach for researchers and the organisations they are a part of.

#### 3.2 Functional Requirements
Our system will be required to accept an initial list of core researchers, and to update this list as required.

Our system will be required to build a database of researchers, branching two degrees of seperation from Dr Ward's core team. It must be able to filter and show visually the relationships between these individuals.

Our system will be required to liase with existing databases of publications, such as pubmed and scopus, through their existing API, to determine the existing co-contributors of any relevant parties.

Our system will be required to filter and visually represent the database as a network map.

#### 3.3 Nonfunctional Requirements
##### 3.3.1 User Interface and Human Factors

Our client has expressed a lack of deep familiarity with computer infrastructure. As such, we must ensure that the client facing elements of the system are simple to explain and use.<br>

Our intent is for the client to have minimal direct contact with the database, unless adding or removing a member of the core research team, which should be simple to do, but clear enough that it will not be done accidentally. Input sections will be clearly labelled, and only accept valid inputs.<br>

The scale of the core research team is small enough that in the worst case, the database can be rebuilt from scratch with reasonable speed, but this should be avoided if at all possible. For this reason, it should be ensured that any interaction with the core research team list should be reversable if required.<br>

The visualiser itself should be clearly and intuitively labelled, with the filters being the same as what the client is already used to searching.<br>

To avoid confusion or overload during the initial database construction, the system should be able to take a simple excel list of members of the core research team, with a tag for their unique researcher ids, and only request clarification if there are issues with any of the initial inputs. <br>

The visualiser must be able to adjust the density of information displayed as reqired.<br>

##### 3.3.2 Documentation

Our client has expressed a lack of deep familiarity with computer infrastructure. As such, we must ensure that the client facing elements of the system are simple to explain and use.<br>

To ensure this, whenever possible, our system should use the same or similar formats as the existing databases our client is familiar with. This ensures that anyone trying to use our system to visualise the existing databases will be able to do so with minimal learning gap. As the user base will consist of existing researchers, this should cover most use cases.<br>

Visualiser configurations should be intuitive, and similar to other systems the users are likely to have use.<br>

Database editing should be required as little as possible, as this is the area potential users are least likely to be already familiar with. Instructions for inputting the initial list of core researchers and for editing this list should be clear and concise. This is fortunately also a rare use case, with the core research team remaining largely stable over time.


##### 3.3.3 Hardware Consideration
Depending on the size of the core research team, our system should be able to maintain a relatively small database, capable of easy storage on the primary work or home computer of any modern researcher, certainly one who intends to use a network visualiser.<br>

Given the actual quantity of information stored for each core researcher, first degree contact, and second degree contact is relatively small (Name, unique ID, position/location, and a list of works co-authored), we should be able to scale the database to fit on a relatively small external drive in the worst case. <br>

It will be important to ensure that our system works on any major operating system. For this reason, the visualiser will run in a webapp, and should be compatable with most major browsers.

##### 3.3.4 Performance Characteristics

Our system would be running primarily in the foreground as a primary task, but will not require particularly high resources. The biggest use of resources will be during the construction of the initial database, which (depending on the size of the core research team) may take a number of minutes, as it must consult the existing online databases for all the publications the core team and their collaborators are involved in. This would only be required on the initial startup, and would afterwards only require checks for publications after the last update.

Our system would require internet connection only for updating the database, and for requesting further information about specific researchers. Given that the pre-existing databases would require constant internet connection, we do not forsee this being an issue.
##### 3.3.5 Error Handling and Extreme Conditions

Our system must be able to handle errors in the initial core researcher list, errors that stem from edits to the core researcher list, and errors that stem from the connections to preexisting databases. <br>

Input errors should be mitigated where possible by ensuring all inputs are vetted before interacting with the database (ie. checking for valid unique researcher id, ensuring new additions to the core list are not already on the list). To avoid issues with the database, it should be easy for the user to undo recent additions or deletions to the core list, and if the database were to have issues, it should be able to revert to a previous state (explaining to the user that it has done so, and why). <br>
In the absolute worst case, the system will be able to reboot the entire database from the list of core researchers, which will take time to be reestablished, so should be avoided. For this reason, the system should store a backup of the database after the initial boot.<br>

Another potential issue the system may face is ballooning of the database if the network becomes too large. In the event that memory required is increasing beyond expectations, the user should be warned, and the system should cease increasing the size of the network without user permission, and adequate space.
##### 3.3.6 System Interfacing

Because our system must request and recieve information from outside systems, it is critical that both the requests sent, and the information recieived is vetted. Requests must be sent in acceptable formats, which requires user inputs to be in a consistent format. This format must be clear to the user. Incoming information must be vetted before being added to the database, to ensure that it is of the type and size requested, and to ensure that it is from the correct source.
##### 3.3.7 Quality Issues

The system should be able to function without direct oversight. The end user is not expected to troubleshoot issues with the system. After an absolutely catastrophic failure, the worst case setup time should be under 10 minutes (the maximum estimate we have for construction of a new database from the list of core researchers)

The system should be capable of being set up on any operating environment, but doesn't need to be directly transferrable. A saved core researcher database should be exportable if required.

The use cases for the system are not high pressure or high-risk.
##### 3.3.8 System Modifications
In future the system could be modified to work with additional exterior databases, and different knowledge bases. This would primarily require changes to our interaction with the API, but our internal database would require very little editing, and the webapp should remain largely the same.
##### 3.3.9 Physical Environment

The expected use of the system is either on a personal or work computer by one or more researchers. The different instances of the system running should not interact. 
##### 3.3.10 Security Issues
There are very few security concerns with the content of the database, as it should only be storing available data (researchers, and the things they have collaborated on). The information also already exists on existing databases, our system should only make that easier to visualise.

Other than that, it is important for general security practices to be followed, especially when interacting with the existing databases. It is important that incoming data is properly vetted.

Physical security is not an issue.
##### 3.3.11 Resource Issues
 

A backup of the initial boot database will be stored, and updated after each boot. Beyond that, the database should be able be backed up by the user at any time. Initial installation should be as simple as providing the client with a copy of the system. The instructions provided should allow the client to easily run through initial setup, but we will also be able to provide direct support until the client is confident with the system.

Continued development and support is not applicable to our current developer-client arrangement, but we are open to further collaboration if requested.

#### 3.4 Constraints

Our system should be able to run on any major OS, for this reason, the webapp and database should be run off a simple linux vm, that should work on any major OS. This should be set up in such a manner that it requires little to no input from the user.

Other than that we shouldn't have any constraints on libraries or development environment.

