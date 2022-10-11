var neoViz;

secondDegree = ""

function hideAll() {
    researcher1.style.display = 'none';
    project.style.display = 'none';
    relationShip_WORKED_WITH.style.display = 'none';
    relationShip_WORKED_ON.style.display = 'none';
    expand.style.display = 'none';
    expand2.style.display = 'none';
}

function layerSoughter(layer) {
    if (layer == 0) {
        return ("Core Researcher")
    }
    else if (layer == 1) {
        return ("First Degree")
    }
    else {
        return ("Second Degree")
    }
}

function newDraw() {
    secondDegree = "";
    draw();
}

function createQuery() {
    const base = "MATCH (a:CoreResearcher) WHERE a.name = '" + document.getElementById('searchBar').value + "' OR  a.id = '" + document.getElementById('searchBar').value + "'"
    //const firstDegree = ""
    const firstDegree = " OPTIONAL MATCH (a:CoreResearcher)-[b: WORKED_WITH] - (c:Researcher)"
    const returnGraph = " RETURN * "
    expandProject = "";
    expandResearcher = "";
    expandProjectRes = "";

    var SD = document.getElementById("secondDegree");
    var expand = document.getElementById("expandResearcher");
    var project = document.getElementById("expandPublications");
    var projectExpansion = document.getElementById("projectExpansion");

    var selectedRes = document.getElementById('res').innerHTML;
    var selectedResDegree = document.getElementById('layerOfKnown').innerHTML;
    var selectedPub = document.getElementById('pub').innerHTML;
    var selectedPubRes = document.getElementById('pubRes').innerHTML;

    console.log(selectedResDegree)

    if (SD.checked) {
        secondDegree = " OPTIONAL MATCH (c:Researcher)-[e: WORKED_WITH] - (f:Researcher)"
        console.log(1)
    } //WHERE toInteger(c.CoAuthors) < 50
    else if (expand.checked == true && (selectedResDegree == "Core Researcher" || selectedResDegree == "First Degree")) {
        secondDegree = " OPTIONAL MATCH (d:Researcher)-[e: WORKED_WITH] - (f:Researcher) WHERE d.id = '" + selectedRes + "'"
        expand4.checked = false;
        console.log(2)
    }
    if (expand.checked && (selectedResDegree == "Second Degree" || SD.checked)) {
        expandResearcher = " OPTIONAL MATCH (g:Researcher)-[h: WORKED_WITH] - (i:Researcher) WHERE g.id = '" + selectedRes + "'"
        //return " MATCH (f:Researcher)-[g: WORKED_WITH] - (h:Researcher) WHERE f.id = '" + selected + "'" + returnGraph
        expand.checked = false;
        console.log(3)
    }
    if (project.checked) {
        expandProject = " OPTIONAL MATCH (j) - [k: WORKED_ON] - (l: Project) WHERE j.id = '" + selectedRes + "'"
        project.checked = false;
        pubRes.innerHTML = selectedRes;
    }
    if (projectExpansion.checked) {
        expandProject = " OPTIONAL MATCH (j) - [k: WORKED_ON] - (l: Project) WHERE j.id = '" + selectedPubRes + "'"
        expandProjectRes = " OPTIONAL MATCH (l: Project) - [m: WORKED_ON] - (n) WHERE l.id = '" + selectedPub + "'"
        projectExpansion.checked = false;
    }

    cypher = base + firstDegree + secondDegree + expandProject + expandResearcher + expandProjectRes + returnGraph
    return cypher
}

function draw() {
    //   Project inbetween
    // 
    //const search = "MATCH (a) WHERE a.name = '" + document.getElementById('searchBar').value + "' OR  a.id = '" + document.getElementById('searchBar').value +  "' OPTIONAL MATCH (a)-[b: WORKED_ON] - (p)- [o: WORKED_ON] - (c) OPTIONAL MATCH (c)-[l: WORKED_ON] - (k)- [q: WORKED_ON] - (e) WHERE NOT e = a RETURN * "
    //Just relationships for scopus db
    //const search = "MATCH (a) WHERE a.name = '" + document.getElementById('searchBar').value + "' OR  a.id = '" + document.getElementById('searchBar').value + "' OPTIONAL MATCH (a)-[b: WORKED_WITH] - (c) OPTIONAL MATCH (c)-[d: WORKED_WITH] - (e) WHERE NOT e = a RETURN * "
    //Just relationships for test
    var search = createQuery()
    const config = {
        containerId: "viz",
        neo4j: {
            serverUrl: "bolt://localhost:7687",
            serverUser: "neo4j",
            serverPassword: "hello"
        },
        
        labels: {
            Researcher: {
                label: "name",
                value: "layerOfKnown",
                group: "layerOfKnown",
            },
            Project: {
                group: "type"
            }
        },
        visConfig: {
            nodes: {
                physics: true,
                shape: "dot",
            },
            edges: {
                physics: true,
                color: "black",
            },
            physics: {
                enabled: true,
                // barnesHut: {
                //     gravitationalConstant: -500000,
                //     centralGravity: 1,
                //     springLength: 100000,
                //     springConstant: 4,
                //     damping: 0.9,
                //     avoidOverlap: 0.9
                // },
                //solver: 'barnesHut',
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {
                    theta: 0.5,
                    gravitationalConstant: -50,
                    centralGravity: 0.01,
                    springConstant: 0.1,
                    springLength: 100,
                    damping: 0.1,
                    avoidOverlap: 0
                },
                maxVelocity: 40,
                minVelocity: 39,
                stabilization: {
                    enabled: true,
                    iterations: 1000,
                    updateInterval: 100,
                    onlyDynamicEdges: false,
                    fit: true
                },
                timestep: 0.25,
                adaptiveTimestep: true,
                wind: { x: 0, y: 0 }
            },
        },
        relationships: {
            WORKED_WITH: {
            },
            WORKED_ON: {
            }
        },
        initialCypher: search
        //Use to return all relationships and researchers
        //initialCypher: "MATCH (n:Researcher), (j)-[r:WORKED_WITH]->(m) RETURN *"
    };
    console.log(search);
    console.log("searched!");
    neoViz = new NeoVis.default(config);
    neoViz.render();

    neoViz.registerOnEvent("clickNode", (properties) => {
        nodeInformation = properties.node.raw
        labels = nodeInformation.labels;
        if (labels.includes("Researcher")) {
            hideAll();
            researcher1.style.display = 'block';
            expand.style.display = 'block';
            scopusID.innerHTML = nodeInformation.properties.id;
            researcherName.innerHTML = nodeInformation.properties.name;
            layerOfKnown.innerHTML = layerSoughter(nodeInformation.properties.layerOfKnown);
            link.innerHTML = nodeInformation.properties.link;
            document.getElementById("link").href = nodeInformation.properties.link;
            res.innerHTML = nodeInformation.properties.id;
            researcherAuthors.innerHTML = nodeInformation.properties.CoAuthors
        }
        else if (labels.includes("Publications") || labels.includes("Project")) {
            hideAll();
            project.style.display = 'block';
            expand2.style.display = 'block';
            projectTitle.innerHTML = nodeInformation.properties.title;
            projectType.innerHTML = nodeInformation.properties.type;
            projectPublisher.innerHTML = nodeInformation.properties.publisher;
            projectID.innerHTML = nodeInformation.properties.id;
            projectLink.innerHTML = nodeInformation.properties.link;
            document.getElementById("projectLink").href = nodeInformation.properties.link;
            pub.innerHTML = nodeInformation.properties.id;
            projectAuthors.innerHTML = nodeInformation.properties.CoAuthors
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