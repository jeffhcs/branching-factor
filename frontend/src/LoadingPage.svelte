<script>
    import LoadingBar from "./LoadingBar.svelte";
    import Syllabus from "./Syllabus.svelte";
    import { loadingTextTrigger } from "./customStore";
    import { progressMap } from "./utils";

    let progress = 0;
    let syllabusText = "";
    const predictedOutputLength = 1600;

    loadingTextTrigger.subscribe((text) => {
        if (text != null) {
            progress = progressMap(text.length, predictedOutputLength, 0.85)
            syllabusText = text;
        }
    })

    // setInterval(() => {
    //     loadingTextTrigger.broadcast(syllabusText + "hello")
    // }, 10)

</script>

<main>
    <div class="container">
        <Syllabus bind:content={syllabusText} />
    <LoadingBar bind:progress={progress} />
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