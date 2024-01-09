<script>
    import { createEventDispatcher } from "svelte";
    import { removePrefixes } from "./parsing/parseSyllabus";
    import LessonModal from "./LessonModal.svelte";
    import { EndpointCaller } from "./backend.js";

    export let chapterData;
    export let notebookId;


    $: chapterName = chapterData
        ? chapterData.chapterName
        : "no chapter selected";
    $: lessons = chapterData ? chapterData.lessons : [];

    const chapterIntroEndpoint = new EndpointCaller("get_chapter_intro");
    chapterIntroEndpoint.onProgress = (responseText) => {
        chapterIntroText = responseText;
    };

    let chapterIntroText = "";

    $: {
        chapterIntroText = "";
        if (chapterData) {
            chapterIntroEndpoint.call({
                notebook_id: notebookId,
                unit_index: chapterData.unit_index,
                chapter_index: chapterData.chapter_index,
            });
        }
    }

    const dispatch = createEventDispatcher();

    function closePanel() {
        dispatch("closePanel");
    }

    let selectedLesson = "";
    $: selectedLessonIndex = lessons.indexOf(selectedLesson);

    function clickLesson(lessonName) {
        selectedLesson = lessonName;
    }
</script>

<main>
    <span class="close" on:click={closePanel}>&times;</span>
    <h2>{chapterName}</h2>
    Lessons:
    <ul>
        {#each lessons as lesson}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <li
                class="lesson"
                on:click={() => {
                    clickLesson(lesson);
                }}
            >
                {lesson}
            </li>
        {/each}
    </ul>
    <p>{chapterIntroText}</p>
    {#if selectedLesson}
        <LessonModal
            bind:lessonName={selectedLesson}
            bind:notebookId
            bind:unit_index={chapterData.unit_index}
            bind:chapter_index={chapterData.chapter_index}
            bind:lesson_index={selectedLessonIndex}
            on:closeModal={() => {
                selectedLesson = "";
            }}
        />
    {/if}
</main>

<style>
    main {
        width: 100%;
        height: 100%;
        border-left: 3px solid black;
        padding: 20px;
        /* margin: 20px; */
        box-sizing: border-box;
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

    .lesson {
        text-decoration: underline;
    }

    .lesson:hover {
        cursor: pointer;
        color: blue;
    }
</style>
