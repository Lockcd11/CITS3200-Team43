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

function search() {

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
                label: 'name',
                group: 'layerOfKnown',
            },
            Project: {
                label: 'projectCategory',
                group: 'projectCategory'
            },
        },
        // }
            // Core_Researcher: {
            //     label: 'name',
            //     group: 'core_researcher'
            // },
            // Researcher: {
            //     label: "name",
            //     group: ""
            // },
            // Project: {
            //     label: "projectCategory",
            //     group: "project"
            // },
        //},

        relationships: {
            WORKED_WITH: {
                value: "20"
            },
            WORKED_ON: {
            }
        },
        initialCypher: "MATCH (n)-[r:WORKED_WITH]->(m)-[k:WORKED_ON]->(h) RETURN n,r,m,k,h"
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