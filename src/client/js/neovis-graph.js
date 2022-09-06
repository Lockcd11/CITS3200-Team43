//! Work in Progress

function draw() {
    var config = {
        container_id: "viz",
        server_url: "bolt://54.88.38.186:32889",
        server_user: "neo4j",
        server_password: "change-guest-honks",
        labels: {
            "Troll": {
                caption: "user_key",
                size: "pagerank",
                community: "community"
            }
        },
        relationships: {
            "RETWEETS": {
                caption: false,
                thickness: "count"
            }
        },
        initial_cypher: "MATCH p=(:Troll)-[:RETWEETS]->(:Troll) RETURN p"
    }

    var viz = new NeoVis.default(config);
    viz.render();
}