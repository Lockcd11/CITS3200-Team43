let svg = d3.select("#svgID");
let width = svg.attr("width");
let height = svg.attr("height");

//! EXAMPLE DATA
let graph = {
    nodes: [
        { name: "John Smith" },
        { name: "Kane Howard" },
        { name: "Evan Barton" },
        { name: "Theo Culley" },
        { name: "Sophia Hoyne" },
        { name: "Tanya Ward" }
    ],
    links: [
        { source: "Tanya Ward", target: "Sophia Hoyne" },
        { source: "Tanya Ward", target: "Kane Howard" },
        { source: "Tanya Ward", target: "Theo Culley" },
        { source: "Tanya Ward", target: "Evan Barton" },
        { source: "John Smith", target: "Sophia Hoyne" }
    ]
}

//? Simulation settings
let simulation = d3
    .forceSimulation(graph.nodes)
    .force("link", d3.forceLink().id(function (d) {
        return d.name;
    })
    .links(graph.links)
    )
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", ticked);

//? Link Elements
let link = svg
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line")
    .attr("stroke-width", function (d) {
        return 4;
    })
    .style("stroke", "pink");

//? Node Elements
let node = svg
    .append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter()
    .append("circle")
    .attr("r", 6)
    .attr("fill", function (d) {
        return "orange"
    })
    .attr("stroke", "yellow");

function ticked() {
    link.attr("x1", function (d) {
        return d.source.x;
    })
        .attr("y1", function (d) {
            return d.source.y;
        })
        .attr("x2", function (d) {
            return d.target.x;
        })
        .attr("y2", function (d) {
            return d.target.y;
        })

    node.attr("cx", function (d) {
        return d.x;
    })
        .attr("cy", function (d) {
            return d.y;
        });
}