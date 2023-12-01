<script>
    import { onMount } from "svelte";
    import cytoscape from "cytoscape";
    import dagre from "cytoscape-dagre";

    let cyContainer;
    let cy;

    const graphLayout = {
        name: "dagre",
        directed: true,
        padding: 10,
        nodeSep: 100,
        rankSep: 100,
        edgeSep: 50,
    };

    const plainData = [
        { group: "nodes", data: { id: "n0" } },
        { group: "nodes", data: { id: "n1" } },
        { group: "edges", data: { id: "e0", source: "n0", target: "n1" } },
    ];

    onMount(() => {
        cytoscape.use(dagre);

        cy = cytoscape({
            container: cyContainer,
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
        });
    });
    export const update_tree = (elements) => {
        cy.elements().remove();
        cy.add(elements);
        cy.layout(graphLayout).run();
    };
</script>

<main>
    <div bind:this={cyContainer} class="cy"></div>
</main>

<style>
    .cy {
        width: 80vw;
        height: 80vh;
        /* border: 2px solid black; */
    }
</style>
