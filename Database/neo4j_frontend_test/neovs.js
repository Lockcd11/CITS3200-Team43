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
    const config = {
        containerId: "viz",
        neo4j: {
            serverUrl: "bolt://localhost:7687",
            serverUser: "neo4j",
            serverPassword: "group43"
        },
        labels: {
            Researcher: {
                label: "name",
                value: "id",
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
        //initialCypher: "MATCH (n)-[r:WORKED_WITH]->(m)-[k:WORKED_ON]->(h)RETURN *"
        initialCypher: "MATCH (n), (j)-[r]->(m) RETURN *"
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