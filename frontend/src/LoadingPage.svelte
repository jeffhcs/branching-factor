<script>
    import LoadingBar from "./LoadingBar.svelte";
    import Syllabus from "./Syllabus.svelte";
    import { loadingTextTrigger } from "./customStore";

    let progress = 0;
    let syllabusText = "hello";
    const predictedOutputLength = 2000;

    loadingTextTrigger.subscribe((text) => {
        if (text != null) {
            progress = progressMap(text.length, predictedOutputLength, 0.80)
            syllabusText = text;
        }
    })

    // setInterval(() => {
    //     loadingTextTrigger.broadcast(syllabusText + "hello")
    // }, 10)

    function progressMap(x, p, q) {
/*
x = current output length
p = predicted output length
q = progress at predicted output length
*/

        const a = 2 * (1 - q)

        const x_1 = x + p * (a - 1)

        const f_asymptote = (a * x_1) / (a * p + x_1)
        const f_linear = x_1 / p

        const f = (x_1 < 0 ? f_linear : f_asymptote) + 1 - a

        return f
    }

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