<script>
    import { onMount, createEventDispatcher } from "svelte";
    import cytoscape from "cytoscape";
    import dagre from "cytoscape-dagre";

    let cyContainer;
    let cy;

    const graphLayout = {
        name: "dagre",
        directed: true,
        padding: 10,
        // nodeSep: 20,
        // rankSep: 60,
        avoidOverlap: true,
        nodeDimensionsIncludeLabels: true,
    };

    const plainData = [
        { group: "nodes", data: { id: "n0" } },
        { group: "nodes", data: { id: "n1" } },
        { group: "edges", data: { id: "e0", source: "n0", target: "n1" } },
    ];

    function removeRedundantEdges(graph) {
        // Convert the graph to an adjacency list for easy traversal
        const adjacencyList = graph.reduce((acc, elem) => {
            if (elem.group === "nodes") {
                acc[elem.data.id] = [];
            }
            if (elem.group === "edges") {
                acc[elem.data.source].push(elem.data.target);
            }
            return acc;
        }, {});

        // Helper function for DFS to find if a path exists from source to target
        function hasPath(source, target, visited = new Set()) {
            if (source === target) return true;
            if (visited.has(source)) return false;

            visited.add(source);
            for (let neighbor of adjacencyList[source]) {
                if (hasPath(neighbor, target, visited)) return true;
            }
            return false;
        }

        // Check and remove redundant edges
        return graph.filter((edge) => {
            if (edge.group === "edges") {
                // Check if a path exists from source to target excluding the direct edge
                const { source, target } = edge.data;
                adjacencyList[source] = adjacencyList[source].filter(
                    (n) => n !== target,
                );
                const pathExists = hasPath(source, target);
                adjacencyList[source].push(target); // Add the direct edge back
                return !pathExists; // Keep the edge if no indirect path exists
            }
            return true; // Keep all nodes
        });
    }

    onMount(() => {
        cytoscape.use(dagre);

        cy = cytoscape({
            container: cyContainer,
            // elements: plainData,
            style: [
                {
                    selector: "node",
                    style: {
                        "background-color": "#666",
                        label: "data(id)",
                    },
                },
                {
                    selector: "edge",
                    style: {
                        width: 3,
                        "line-color": "#ccc",
                        "target-arrow-color": "#ccc",
                        "target-arrow-shape": "triangle",
                        "arrow-scale": 4,
                        "curve-style": "bezier",
                    },
                },
            ],
            layout: graphLayout,
            wheelSensitivity: 0.2,
        });
        cy.on("tap", "node", function (event) {
            var node = event.target;
            var chapterName = node.data("id");
            var lessons = node.data("lessons");
            clickChapter({ chapterName, lessons });
            // display_model(label + " (" + document.getElementById('prompt').value + ")");
        });
    });

    export const update_tree = (elements) => {
        cy.elements().remove();
        cy.add(removeRedundantEdges(elements));
        cy.layout(graphLayout).run();
    };
    const dispatch = createEventDispatcher();

    function clickChapter(nodeData) {
        dispatch("chapterClicked", nodeData);
    }

</script>

<div bind:this={cyContainer} class="cy"></div>


<style>
    .cy {
        width: 100%;
        height: 100%;
        /* border: 2px solid black; */
    }

</style>
