<script>
    import { element } from "svelte/internal";
    import LessonTree from "./LessonTree.svelte";
    import YAML from "js-yaml";
    let lessonTreeComponent;

    function parseToTreeElements(llmOutput) {
        try {
            var newlineCount = (llmOutput.match(/\n/g) || []).length;
            if (newlineCount < 2) {
                return false;
            }

            var cleanedText = llmOutput.substring(
                0,
                llmOutput.lastIndexOf("\n\n") + 1,
            );

            const tree = YAML.load(cleanedText);

            const elements = [];

            for (const lesson in tree.LessonTree) {
                const prerequisites = tree.LessonTree[lesson];

                elements.push({
                    group: "nodes",
                    data: { id: lesson },
                });

                prerequisites.forEach((prereq) => {
                    elements.push({
                        group: "edges",
                        data: { source: prereq, target: lesson },
                    });
                });
            }

            return elements;
        } catch (e) {
            console.log(llmOutput, e);
            return false;
        }
    }
    let generateTreeXhr = new XMLHttpRequest();
    function callGenerateTreeEndpoint(prompt) {
        generateTreeXhr.abort();
        generateTreeXhr = new XMLHttpRequest();
        generateTreeXhr.open(
            "GET",
            "http://127.0.0.1:5000/generate_tree?prompt=" +
                encodeURIComponent(prompt),
            true,
        );
        generateTreeXhr.onprogress = function () {
            console.log(generateTreeXhr.responseText);
            const elements = parseToTreeElements(generateTreeXhr.responseText);
            if (elements) lessonTreeComponent.update_tree(elements);
        };
        generateTreeXhr.send();
    }
    let courseNamePrompt = "real analysis";

    function generateTree() {
        callGenerateTreeEndpoint(courseNamePrompt);
    }
</script>

<main>
    What do you want to learn?
    <input type="text" bind:value={courseNamePrompt}/>
    <button on:click={generateTree}>Generate</button>
    <LessonTree bind:this={lessonTreeComponent} />
</main>

<style>
    main {
        font-family: "Arial", sans-serif;
        background-color: #f4f4f4;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
        color: #333;
    }

    input[type="text"] {
        padding: 10px;
        margin: 10px 0;
        border: none;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    }

    button {
        padding: 10px 15px;
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        color: white;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #0056b3;
    }
</style>
