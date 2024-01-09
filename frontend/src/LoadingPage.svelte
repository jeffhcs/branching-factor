<script>
    import LoadingBar from "./LoadingBar.svelte";
    import Syllabus from "./Syllabus.svelte";
    import { progressMap } from "./utils";
    import {
        splashPromptTrigger,
        currentPageTrigger,
        notebookTrigger,
    } from "./customStore";
    import { EndpointCaller } from "./backend";
    import {
        parseSyllabusYaml,
        getChaptersForTree,
    } from "./parsing/parseSyllabus";
    import yaml from "js-yaml";

    let progress = 0;
    let syllabusText = "";
    const predictedOutputLength = 1600;

    // loadingTextTrigger.subscribe((text) => {
    //     if (text != null) {
    //         progress = progressMap(text.length, predictedOutputLength, 0.85)
    //         syllabusText = text;
    //     }
    // })
    const syllabusEndpoint = new EndpointCaller("create_notebook");
    syllabusEndpoint.onProgress = (responseText) => {
        syllabusText = responseText;
        progress = progressMap(
            syllabusText.length,
            predictedOutputLength,
            0.85,
        );
    };
    syllabusEndpoint.onDone = (responseText) => {
        console.log("DONE");

        const notebook = yaml.load(responseText);

        notebookTrigger.broadcast(notebook.notebook_id);
        currentPageTrigger.broadcast("main");

        // console.log(syllabusText);
        // const syllabusTextTemp = "Syllabus:" + extractText(syllabusText, "syllabus:", "\n\n");
        // console.log(syllabusTextTemp);
        // const syllabus = parseSyllabusYaml(syllabusTextTemp);
        // const chaptersData = getChaptersForTree(syllabus);
        // console.log(chaptersData);
        // syllabus = parseSyllabusYaml(syllabusText);
        // if (syllabus) {
        // courseObjectTrigger.broadcast(syllabus);
        // const chaptersPrompt = getChaptersForTree(syllabus);
        // callGenerateTreeEndpoint(chaptersPrompt);
        // }
    };
    function extractText(str, flag1, flag2) {
        const regex = new RegExp(`${flag1}([\\s\\S]*?)${flag2}`);
        const match = regex.exec(str);
        return match ? match[1] : null;
    }

    splashPromptTrigger.subscribe((promptText) => {
        if (promptText != null) {
            const access_token = JSON.parse(localStorage.getItem("oauth2-test-params"))["access_token"];

            currentPageTrigger.broadcast("loading");
            syllabusEndpoint.call({ prompt: promptText, access_token: access_token});
        }
    });
</script>

<main>
    <div class="container">
        <Syllabus bind:content={syllabusText} />
        <LoadingBar bind:progress />
    </div>
</main>

<style>
    body {
        font-family: "Arial", sans-serif;
        background-color: #f0f0f0;
        color: #333;
        text-align: center;
        padding: 50px;
    }

    .container {
        position: relative;
        top: 20vh;
        width: 50vh;
        height: 50vh;
        border: 3px solid black;
        padding: 10px;
        display: grid;
        grid-template-rows: 80% 20%;
        place-items: center;
        max-width: 100%;
        margin: 0 auto;
    }
</style>
