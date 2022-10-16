from neo4j import GraphDatabase
import os

def path(tx):
    result = tx.run("""
            Call dbms.listConfig() YIELD name, value
            WHERE name='dbms.directories.neo4j_home'
            RETURN value""")
    return result.values()

def get_import_file_location():
    
    db_details = {'db': None, 'password': None, 'port': None}
    with open("db_details.txt", 'r') as f:
        for i in f.readlines():
            info = i.strip().split(',')
            db_details[info[0]] = info[1]
    
    driver = GraphDatabase.driver(db_details['port'], auth=(db_details['db'], db_details['password']))
    
    session = driver.session()
    
    result = session.read_transaction(path)
    
    value = result[0][0] + "\import"
    
    if os.path.exists("filePath.txt"):
        os.remove("filePath.txt")
    
    #text_file = open("filePath.txt", "w")
    #text_file.write(value)
    #text_file.close()

    session.close()
    return value
