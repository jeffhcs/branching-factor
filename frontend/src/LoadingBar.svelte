<script>
    export let progress = 50;
    // const elem = document.getElementById("progressBar");
    let bar;

    const updateProgress = () => {
        if (bar != null) {
            bar.style.width = progress * 100 + "%";
        }
        return progress;
    };

    $: progress = updateProgress(progress);
</script>

<div id="progressBar">
    <div bind:this={bar} id="progressBarFill"></div>
</div>

<style>
    #progressBar {
        width: 100%;
        background-color: #ddd;
        border: 2px solid black;
    }

    #progressBarFill {
        width: 0%;
        height: 30px;
        background-color: black;
    }

    button {
        background-color: black;
        color: white;
        border: none;
        padding: 10px 20px;
        margin-top: 20px;
        cursor: pointer;
    }

    button:hover {
        background-color: #444;
    }
</style>
