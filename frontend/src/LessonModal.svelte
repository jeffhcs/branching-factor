<script>
    import { createEventDispatcher } from "svelte";
    import { removePrefixes } from "./parsing/parseSyllabus";
    import LoadingBar from "./LoadingBar.svelte";
    import { progressMap } from "./utils";

    export let lessonName;
    export let syllabusText;

    let oldLessonName = "";

    const dispatch = createEventDispatcher();

    function closeModal() {
        lessonContentXhr.abort();
        dispatch("closeModal");
    }
    let lessonContentXhr = new XMLHttpRequest();

    let lessonContent = "";
    let progress = 0;
    const predictedOutputLength = 1800;
    let finishedGenerating = false;

    $: {
        if (lessonName && syllabusText && lessonName != oldLessonName) {
            oldLessonName = lessonName;
            lessonContentXhr.abort();
            lessonContentXhr = new XMLHttpRequest();
            lessonContentXhr.open(
                "GET",
                "http://127.0.0.1:5000/generate_lesson?prompt=" +
                    encodeURIComponent(lessonName) +
                    "&syllabus=" +
                    encodeURIComponent(removePrefixes(syllabusText)),
                true,
            );
            lessonContentXhr.onprogress = function () {
                console.log(lessonContentXhr.responseText);
                lessonContent = lessonContentXhr.responseText;
                progress = progressMap(
                    lessonContent.length,
                    predictedOutputLength,
                    0.85,
                );
                console.log(
                    lessonContent.length,
                    predictedOutputLength,
                    progress,
                );
            };
            lessonContentXhr.onreadystatechange = function () {
                if (lessonContentXhr.readyState === XMLHttpRequest.DONE) {
                    if (lessonContentXhr.status === 200) {
                        finishedGenerating = true;
                    } else {
                        console.log("There was a problem with the request.");
                    }
                }
            };
            lessonContentXhr.send();
        }
    }
</script>

<div id="myModal" class="modal">
    <div class="modal-content">
        <span id="closeModal" class="close" on:click={closeModal}>&times;</span>
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
        margin: 10vh auto;
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
