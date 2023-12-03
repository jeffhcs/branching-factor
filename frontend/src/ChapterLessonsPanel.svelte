<script>
    import { createEventDispatcher } from "svelte";

    export let chapterData;
    $: chapterName = chapterData
        ? chapterData.chapterName
        : "no chapter selected";
    $: lessons = chapterData ? chapterData.lessons : [];

    const dispatch = createEventDispatcher();

    function closePanel() {
        dispatch("closePanel");
    }
</script>

<main>
    <span class="close" on:click={closePanel}>&times;</span>
    <h2>{chapterName}</h2>
    Lessons:
    <ul>
        {#each lessons as lesson}
            <li>{lesson}</li>
        {/each}
    </ul>
</main>

<style>
    main {
        width: 100%;
        height: 100%;
        border: 1px solid black;
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
</style>
