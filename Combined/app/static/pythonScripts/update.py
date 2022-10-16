from neo4j import GraphDatabase
import os
import csv
from fileGrab import get_import_file_location
from transferCSVs import transfer_csvs

def update_project(tx):
    return tx.run("""
        LOAD CSV WITH HEADERS FROM 'file:///add/publications.csv' AS row
        MERGE (publications:Project {
            id: row.id,
            title: row.title,
            type: row.type,
            publisher: row.publisher,
            link: row.link,
            CoAuthors: row.author_count
        })
            """)

def update_researcher(tx):
    return tx.run("""
        LOAD CSV WITH HEADERS FROM 'file:///add/researchers.csv' AS row
        MERGE (researchers:Researcher {
            id: row.id,
            name: row.name,
            link: row.link,
            layerOfKnown: row.degrees,
            CoAuthors: row.coauthor_count
        })
            """)

def core_researcher(tx):
    return tx.run("""
        MATCH (n:Researcher)
            WHERE n.layerOfKnown = "3"
                SET n:CoreResearcher
            """)

def first_degree(tx):
    return tx.run("""
        MATCH (n:Researcher)
            WHERE n.layerOfKnown = "2"
                SET n:FirstDegree
            """)

def second_degree(tx):
    return tx.run("""
        MATCH (n:Researcher)
            WHERE n.layerOfKnown = "1"
                SET n:SecondDegree
            """)

def clear1(tx):
    return tx.run("""
        MATCH (n:FirstDegree), (a:SecondDegree) WHERE n.id = a.id DETACH DELETE a
            """)

def clear2(tx):
    return tx.run("""
        MATCH (n:CoreResearcher), (a:SecondDegree) WHERE n.id = a.id DETACH DELETE a
            """)

def clear3(tx):
    return tx.run("""
        MATCH (n:CoreResearcher), (a:FirstDegree) WHERE n.id = a.id DETACH DELETE a
            """)

def update_worked_on(tx):
    return tx.run("""
        LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
         MATCH (a:Researcher{id: row.author_id})
         MATCH (b:Project{id:row.publication_eid})
         MERGE (a)-[r:WORKED_ON]->(b)
            """)

def update_worked_with(tx):
    return tx.run("""
    MATCH
     (a:Researcher)-[r:WORKED_ON]->(p:Project),
     (b:Researcher)-[l:WORKED_ON]->(p:Project)
        MERGE (a)-[k:WORKED_WITH]-(b)
            """)

def clearDups(tx):
    return tx.run("""
    MATCH (n1:Researcher),(n2:Researcher)
    WHERE n1.id = n2.id and id(n1) < id(n2)
    DETACH DELETE n2
            """)

def adjustCoAuthors(tx):
    return tx.run("""
    MATCH (a:Researcher)-[:WORKED_WITH]-(b:Researcher)
    WITH a, count(b) as rels
    SET a.CoAuthors = rels
            """)

def update_db():
    
    transfer_csvs(2)
    
    db_details = {'db': None, 'password': None, 'port': None}
    with open("db_details.txt", 'r') as f:
        for i in f.readlines():
            info = i.strip().split(',')
            db_details[info[0]] = info[1]
    
    driver = GraphDatabase.driver(db_details['port'], auth=(db_details['db'], db_details['password']))
    
    session = driver.session()
    
    project = session.write_transaction(update_project)
    print("Project created\n")
    researcher = session.write_transaction(update_researcher)
    print("Researcher created\n")
    core = session.write_transaction(core_researcher)
    print("Core done\n")
    first = session.write_transaction(first_degree)
    print("First done\n")
    second = session.write_transaction(second_degree)
    print("Second done\n")
    clear_1 = session.write_transaction(clear1)
    print("Clear 1 done\n")
    clear_2 = session.write_transaction(clear2)
    print("Clear 2 done\n")
    clear_3 = session.write_transaction(clear3)
    print("Clear 3 done\n")
    clear_dups = session.write_transaction(clearDups)
    print("Cleared Dups\n")
    adjusted_coauthors = session.write_transaction(adjustCoAuthors)
    print("Adjusted Co Authors\n")
    worked_on = session.write_transaction(update_worked_on)
    print("Worked on created\n")
    worked_with = session.write_transaction(update_worked_with)
    print("Worked with created\n") 
    
    session.close()
    
    return 1
