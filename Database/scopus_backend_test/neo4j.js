
const driver = neo4j.driver("bolt://localhost:7687", neo4j.auth.basic("neo4j", "group43"))


function run_command(command, para) {
    session = driver.session();
    if (para == undefined) {
        done = session.run(command)
    }
    else {
        done = session.run(command, para)
    }
}

function create_researcher() {


    // Submits scopus to Cam's add function

    run_command('MATCH (n) DETACH DELETE n');
    run_command('LOAD CSV WITH HEADERS FROM "file:///project.csv" AS row CREATE(project: Project {id: row.projectID,projectCategory: row.projectCategory, publicationYear: row.publicationYear})');
    run_command('LOAD CSV WITH HEADERS FROM "file:///researcher.csv" AS row CREATE(researcher: Researcher { id: row.researcherID, name: row.researcherName, scopusID: row.scopusID, layerOfKnown: row.layerOfKnown })');
    run_command('LOAD CSV WITH HEADERS FROM "file:///worked_on.csv" AS row MATCH (a: Researcher), (b: Project) WHERE row.researcher = a.id AND row.project = b.id CREATE(a) - [r: WORKED_ON] -> (b)');
    run_command('LOAD CSV WITH HEADERS FROM "file:///worked_with.csv" AS row MATCH (a: Researcher), (b: Researcher)  WHERE row.researcherOne = a.id AND row.researcherTwo = b.id  CREATE(a) - [r: WORKED_WITH { numberOfTimes: row.numberOfTimes }] -> (b)');
    run_command('MATCH (n:Researcher) WHERE n.layerOfKnown = "2" SET n: FirstDegree RETURN n');
    run_command('MATCH (n:Researcher) WHERE n.layerOfKnown = "3" SET n: SecondDegree RETURN n');
    run_command('MATCH (n:Researcher) WHERE n.layerOfKnown = "1" SET n: CoreResearcher RETURN n');
    console.log("Done");
    //temp add for testing purposes. Normally it would update the csv so it'll auto add
    run_command('Create (n:Researcher {id:20, name: "Kane", scopusID: $scopusID, layerOfKnown: "1" })', { scopusID: document.getElementById('scopusID').value });
    console.log("added");
    //Uncomment from here

    //to here
}
function remove_researcher() {
    const scopusID = document.getElementById('scopusID').value
    // Submits scopus to Cam's remove function

    //uncomment for proper run
    //run_command('MATCH (n) DETACH DELETE n')
    //run_command('LOAD CSV WITH HEADERS FROM "file:///project.csv" AS row CREATE(project: Project {id: row.projectID,projectCategory: row.projectCategory, publicationYear: row.publicationYear})')
    //run_command('LOAD CSV WITH HEADERS FROM "file:///researcher.csv" AS row CREATE(researcher: Researcher { id: row.researcherID, name: row.researcherName, scopusID: row.scopusID, layerOfKnown: row.layerOfKnown })')
    //run_command('LOAD CSV WITH HEADERS FROM "file:///worked_on.csv" AS row MATCH (a: Researcher), (b: Project) WHERE row.researcher = a.id AND row.project = b.id CREATE(a) - [r: WORKED_ON] -> (b)')
    //run_command('LOAD CSV WITH HEADERS FROM "file:///worked_with.csv" AS row MATCH (a: Researcher), (b: Researcher)  WHERE row.researcherOne = a.id AND row.researcherTwo = b.id  CREATE(a) - [r: WORKED_WITH { numberOfTimes: row.numberOfTimes }] -> (b)')
    //run_command('MATCH (n:Researcher) WHERE n.layerOfKnown = "2" SET n: FirstDegree RETURN n')
    //run_command('MATCH (n:Researcher) WHERE n.layerOfKnown = "3" SET n: SecondDegree RETURN n')
    //run_command('MATCH (n:Researcher) WHERE n.layerOfKnown = "1" SET n: CoreResearcher RETURN n')

    //For test
    run_command('MATCH (n:Researcher {scopusID: $scopusID}) DETACH DELETE n', { scopusID: scopusID })
}