let neoViz;


function hideAll() {
    researcher.style.display = 'none';
    project.style.display = 'none';
    relationShip_WORKED_WITH.style.display = 'none';
    relationShip_WORKED_ON.style.display = 'none';
}

function layerSoughter(layer) {
    if (layer == 1) {
        return ("Core Researcher")
    }
    else if (layer == 2) {
        return ("First Layer")
    }
    else {
        return ("Second Layer")
    }
}

function draw() {
    //   Project inbetween
    //   const search = "MATCH (a) WHERE a.id = '" + document.getElementById('searchBar').value + "' OPTIONAL MATCH (a)-[b: WORKED_ON] - (p)- [o: WORKED_ON] - (c) OPTIONAL MATCH (c)-[l: WORKED_ON] - (k)- [q: WORKED_ON] - (e) WHERE NOT e = a RETURN * "
    //   Just relationships for scopus db
    //   const search = "MATCH (a) WHERE a.id = '" + document.getElementById('searchBar').value + "' OPTIONAL MATCH (a)-[b: WORKED_WITH] - (c) OPTIONAL MATCH (c)-[d: WORKED_WITH] - (e) WHERE NOT e = a RETURN * "
    //   Just relationships for test
    const search = "MATCH (a:CoreResearcher) WHERE a.name = '" + document.getElementById('searchBar').value + "' OPTIONAL MATCH (a)-[b: WORKED_WITH] - (c) OPTIONAL MATCH (c)-[d: WORKED_WITH] - (e) WHERE NOT e = a RETURN * "
    const config = {
        containerId: "viz",
        neo4j: {
            serverUrl: "bolt://localhost:7687",
            serverUser: "neo4j",
            serverPassword: "group43"
            //serverPassword: "adam"
        },
        labels: {
            Researcher: {
                label: "name",
                value: "layerOfKnown",
                group: "layerOfKnown"
            },
            Project: {
                label: "projectCategory",
                value: "id",
                group: "projectCategory"
            }
        },
        visConfig: {
            nodes: {
                shape: 'square',
            }
        },
        relationships: {
            WORKED_WITH: {
                group: "name"
            },
            WORKED_ON: {
            }
        },
        initialCypher: search
        //Use to return all relationships and researchers
        //initialCypher: "MATCH (n:Researcher), (j)-[r:WORKED_WITH]->(m) RETURN *"
    };

    neoViz = new NeoVis.default(config);
    neoViz.render();

    neoViz.registerOnEvent("clickNode", (properties) => {
        nodeInformation = properties.node.raw
        labels = nodeInformation.labels;
        if (labels.includes("Researcher")) {
            hideAll();
            researcher.style.display = 'block';
            scopusID.innerHTML = nodeInformation.properties.scopusID
            researcherName.innerHTML = nodeInformation.properties.name
            layerOfKnown.innerHTML = layerSoughter(nodeInformation.properties.layerOfKnown)
        }
        else if (labels.includes("Project")) {
            hideAll();
            project.style.display = 'block';
            projectCategory.innerHTML = nodeInformation.properties.projectCategory
            publicationYear.innerHTML = nodeInformation.properties.publicationYear
        }
    });

    neoViz.registerOnEvent("clickEdge", (properties) => {
        const edgeInformation = properties.edge;
        if (edgeInformation.raw.type == "WORKED_ON") {
            hideAll();
            relationShip_WORKED_ON.style.display = 'block';
            r.innerHTML = edgeInformation.from;
            projectName.innerHTML = edgeInformation.to;
        }
        else if (edgeInformation.raw.type == "WORKED_WITH") {
            hideAll();
            relationShip_WORKED_WITH.style.display = 'block';
            r1.innerHTML = edgeInformation.from;
            r2.innerHTML = edgeInformation.to;
            workedWith.innerHTML = edgeInformation.value;
        }
    });
}