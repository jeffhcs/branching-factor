<script>
    import { createEventDispatcher } from "svelte";
    import { removePrefixes } from "./parsing/parseSyllabus";

    export let lessonName;
    export let syllabusText;
    const dispatch = createEventDispatcher();

    function closeModal() {
        lessonContentXhr.abort();
        dispatch("closeModal");
    }
    let lessonContentXhr = new XMLHttpRequest();

    let lessonContent = "";

    $: {
        if (lessonName && syllabusText) {
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
            };
            lessonContentXhr.send();
        }
    }
</script>

<div id="myModal" class="modal">
    <div class="modal-content">
        <span id="closeModal" class="close" on:click={closeModal}>&times;</span>
        {@html lessonContent}
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

    /* Modal content */
    .modal-content {
        background-color: #fefefe;
        margin: 15% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 80%;
    }

    /* Close button */
    .close {
        color: #aaa;
        float: right;
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
