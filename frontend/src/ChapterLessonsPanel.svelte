<script>
    import { createEventDispatcher } from "svelte";
    import { removePrefixes } from "./parsing/parseSyllabus";
    import LessonModal from "./LessonModal.svelte";

    export let chapterData;
    export let syllabusText;
    $: chapterName = chapterData
        ? chapterData.chapterName
        : "no chapter selected";
    $: lessons = chapterData ? chapterData.lessons : [];

    let chapterIntroXhr = new XMLHttpRequest();

    let chapterIntroText = "";

    $: {
        chapterIntroText = "";
        if (chapterName && syllabusText) {
            chapterIntroXhr.abort();
            chapterIntroXhr = new XMLHttpRequest();
            chapterIntroXhr.open(
                "GET",
                "http://127.0.0.1:5000/generate_chapter_intro?chapter=" +
                    encodeURIComponent(chapterName) +
                    "&syllabus=" +
                    encodeURIComponent(removePrefixes(syllabusText)),
                true,
            );
            chapterIntroXhr.onprogress = function () {
                chapterIntroText = chapterIntroXhr.responseText;
            };
            chapterIntroXhr.send();
        }
    }

    const dispatch = createEventDispatcher();

    function closePanel() {
        dispatch("closePanel");
    }

    let selectedLesson = "";

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
            bind:syllabusText={syllabusText}
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
