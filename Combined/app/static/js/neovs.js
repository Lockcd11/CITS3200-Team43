var neoViz;
var portNumber = "bolt://localhost:7687"; 
var password='group43';
secondDegree = ""

//function getPort() {
//    var input = document.getElementById("portNumber").value;
//    portNumber = "bolt://localhost:" + input;
//    console.log(portNumber)
//}
//function getPassword() {
//    var input = document.getElementById("password").value;
//    password = input;
//}

function hideAll() {
    researcher.style.display = 'none';
    project.style.display = 'none';
    expand.style.display = 'none';
    expand2.style.display = 'none';
}

function layerSoughter(layer) {
    if (layer == 3) {
        return ("Core Researcher")
    }
    else if (layer == 2) {
        return ("First Degree")
    }
    else if (layer == 1) {
        return ("Second Degree")
    }
    else {
        return("Extra")
    }
}

function newDraw() {
    secondDegree = "";
    draw();
}

function createQuery() {
    const base = "MATCH (a:CoreResearcher) WHERE a.name = '" + document.getElementById('searchBar').value + "' OR  a.id = '" + document.getElementById('searchBar').value + "'"
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
    }
    else if (expand.checked == true && (selectedResDegree == "Core Researcher" || selectedResDegree == "First Degree")) {
        secondDegree = " OPTIONAL MATCH (d:Researcher)-[e: WORKED_WITH] - (f:Researcher) WHERE d.id = '" + selectedRes + "'"
        expand.checked = false;
        console.log(2)
    }
    if (expand.checked && (selectedResDegree == "Second Degree" || SD.checked)) {
        expandResearcher = " OPTIONAL MATCH (g:Researcher)-[h: WORKED_WITH] - (i:Researcher) WHERE g.id = '" + selectedRes + "'"
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
    var search = createQuery()
    const config = {
        containerId: "viz",
        neo4j: {
            serverUrl: portNumber,
            serverUser: "neo4j",
            serverPassword: password
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
            researcher.style.display = 'block';
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

    //document.getElementById("password_submit").addEventListener("submit", getPassword);
    //document.getElementById("port_submit").addEventListener("submit", getPort);
}