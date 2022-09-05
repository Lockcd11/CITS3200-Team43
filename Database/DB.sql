DROP TABLE IF EXISTS fact_worked_on;
DROP TABLE IF EXISTS fact_worked_with;
DROP TABLE IF EXISTS dim_project;
DROP TABLE IF EXISTS dim_researcher;
DROP TABLE IF EXISTS dim_core_researcher;

CREATE TABLE dim_project(
    projectID int IDENTITY(1,1) PRIMARY KEY,
	projectCategory varchar(255) NOT NULL,
	publicationYear int NOT NULL, -- could be: publicationDate date NOT NULL
); 
	
CREATE TABLE dim_researcher(
    researcherID int IDENTITY(1,1) PRIMARY KEY,
	researcherName varchar(255) NOT NULL,
	scopusID int NOT NULL,
	layerOfKnown int NOT NULL,
);

CREATE TABLE fact_worked_on(
    researcher int FOREIGN KEY REFERENCES dim_researcher(researcherID) NOT NULL,
	project int FOREIGN KEY REFERENCES dim_project(projectID) NOT NULL,
);

CREATE TABLE fact_worked_with(
    researcherOne int FOREIGN KEY REFERENCES dim_researcher(researcherID) NOT NULL,
	researcherTwo int FOREIGN KEY REFERENCES dim_researcher(researcherID) NOT NULL,
	numberOfTimes int,
);

CREATE TABLE dim_core_researcher(
    researcherID int IDENTITY(1,1) PRIMARY KEY,
	researcherName varchar(255) NOT NULL,
	scopusID int NOT NULL,
);