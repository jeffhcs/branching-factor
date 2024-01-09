<script>
    import LessonTree from "./LessonTree.svelte";
    import yaml from "js-yaml";
    import ChapterLessonsPanel from "./ChapterLessonsPanel.svelte";
    import Syllabus from "./Syllabus.svelte";
    import {
        parseSyllabusYaml,
        getChaptersForTree,
    } from "./parsing/parseSyllabus";
    import {
        splashPromptTrigger,
        loadingTextTrigger,
        currentPageTrigger,
        courseObjectTrigger,
    } from "./customStore.js";
    import { EndpointCaller } from "./backend.js";

    let lessonTreeComponent;
    export let notebook_id;

    const treeEndpoint = new EndpointCaller("get_tree");
    treeEndpoint.onProgress = (responseText) => {
        // const elements = parseToTreeElements(responseText);
        // if (elements) lessonTreeComponent.update_tree(elements);
        // console.log(responseText);
        const elements = JSON.parse(responseText);
        lessonTreeComponent.update_tree(elements);
    };

    $: if (notebook_id) {
        treeEndpoint.call({ notebook_id: notebook_id});
    }

    let courseNamePrompt = "";
    let syllabusText = "";
    let syllabus;

    let selectedChapterData;

    function handleChapterClicked(event) {
        selectedChapterData = event.detail;
    }

    function handleClosePanel() {
        selectedChapterData = null;
    }

</script>

<main>
    <!-- <div>
        Where's Curiosity Taking You?
        <input type="text" bind:value={courseNamePrompt} />
        <button on:click={generate}>Generate</button>
    </div> -->
    <div class="tree-window">
        <div class="lesson-tree">
            <LessonTree
                bind:this={lessonTreeComponent}
                on:chapterClicked={handleChapterClicked}
            />
        </div>
        {#if selectedChapterData}
            <div class="chapter-panel">
                <ChapterLessonsPanel
                    bind:chapterData={selectedChapterData}
                    bind:notebookId={notebook_id}
                    on:closePanel={handleClosePanel}
                />
            </div>
        {/if}
    </div>
    <!-- <Syllabus bind:content={syllabusText} /> -->
</main>

<style>
    main {
        font-family: sans-serif;
        /* background-color: #f4f4f4; */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        /* margin: 0; */
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
    .tree-window {
        display: flex;
        /* justify-content: space-between; 
        align-items: start;  */
        border: black solid 3px;
        width: 80vw;
        height: 90vh;
        margin-bottom: 5vh;
    }

    .lesson-tree {
        flex-grow: 2;
        flex-basis: 0;
        flex-shrink: 1;
        overflow: hidden;
    }
    .chapter-panel {
        flex-grow: 1;
        flex-basis: 0;
        flex-shrink: 0;
    }
</style>
