<script>
    import { createEventDispatcher } from "svelte";
    import { removePrefixes } from "./parsing/parseSyllabus";
    import LoadingBar from "./LoadingBar.svelte";
    import { progressMap } from "./utils";
    import { EndpointCaller } from "./backend.js";

    export let lessonName;
    export let notebookId;
    export let unit_index;
    export let chapter_index;
    export let lesson_index;

    let oldLessonName = "";

    const dispatch = createEventDispatcher();

    function closeModal() {
        lessonEndpoint.abort();
        dispatch("closeModal");
    }

    const lessonEndpoint = new EndpointCaller("get_lesson");
    lessonEndpoint.onProgress = (responseText) => {
        lessonContent = responseText;
        progress = progressMap(
            lessonContent.length,
            predictedOutputLength,
            0.85,
        );
    };
    lessonEndpoint.onDone = (responseText) => {
       finishedGenerating = true;
    };

    let lessonContent = "";
    let progress = 0;
    const predictedOutputLength = 1800;
    let finishedGenerating = false;

    $: {
        if (notebookId) {
            // oldLessonName = lessonName;
            lessonEndpoint.call({
                notebook_id: notebookId,
                unit_index: unit_index,
                chapter_index: chapter_index,
                lesson_index: lesson_index,
            });
        }
    }
</script>

<div id="myModal" class="modal">
    <div class="modal-content">
        <span class="close" on:click={closeModal}>&times;</span>
        {@html lessonContent}
        {#if !finishedGenerating}
            <div class="loading-bar">
                <LoadingBar bind:progress />
            </div>
        {/if}
    </div>
</div>

<style>
    /* Modal style */
    .modal {
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.4);
    }

    .loading-bar {
        margin-top: auto; /* Pushes the bottom div to the bottom */
    }

    /* Modal content */
    .modal-content {
        background-color: #fefefe;
        margin: 5vh auto;
        padding: 40px;
        border: 3px solid black;
        width: 80%;
        min-height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between; /* Aligns children from start to end */
    }

    /* Close button */
    .close {
        color: #aaa;
        text-align: right;
        font-size: 28px;
        font-weight: bold;
    }

    .close:hover,
    .close:focus {
        color: black;
        text-decoration: none;
        cursor: pointer;
    }
</style>
