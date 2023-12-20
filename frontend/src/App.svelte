<script>
    import MainPrompt from "./MainPrompt.svelte";
    import Splash from "./Splash.svelte";

    import { splashPromptTrigger } from "./customStore.js";

    let currPage = "splash";

    splashPromptTrigger.subscribe((promptText) => {
        if (promptText != null) {
            currPage = "main";
        }
    });
</script>

<main>
    {#if currPage === "main"}
        <MainPrompt />
    {:else if currPage === "splash"}
        <Splash />
    {/if}
</main>

<style>
    main {
        /* border-style: solid; */
        height: 97vh;
        width: 100vw;
    }
</style>
