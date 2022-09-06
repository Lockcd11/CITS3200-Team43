USE [Proffesional_Computing_DB]
GO

INSERT INTO [dbo].[dim_core_researcher]
           ([researcherName]
           ,[scopusID])
     VALUES
           ('Adam McAlpine',22705392)
GO

INSERT INTO [dbo].[dim_project]
           ([projectCategory]
           ,[publicationYear])
     VALUES
           ('Science', 2022),
		   ('Law', 2017),
		   ('Social Science', 2019)
GO

INSERT INTO [dbo].[dim_researcher]
           ([researcherName]
           ,[scopusID]
           ,[layerOfKnown])
     VALUES
           ('Adam McAlpine',22705392, 1),
		   ('Dean McAlpine',22705393, 2),
		   ('Lachlan McAlpine',22705394, 2),
		   ('Cameron Locke',21137282, 2),
		   ('Bob',6738192, 3)
GO

INSERT INTO [dbo].[fact_worked_on]
           ([researcher]
           ,[project])
     VALUES
           (1, 1),
		   (1, 3),
		   (2, 3),
		   (3, 1),
		   (4, 1),
		   (4, 2),
		   (5, 2)
GO

INSERT INTO [dbo].[fact_worked_with]
           ([researcherOne]
           ,[researcherTwo]
           ,[numberOfTimes])
     VALUES
           ( 1, 3, 1),
		   ( 1, 4, 1),
		   ( 1, 2, 1),

		   ( 3, 4, 1),

		   ( 4, 5, 1)
GO
