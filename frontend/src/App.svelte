<script>
    import CoverPage from "./CoverPage.svelte";
    import LoadingPage from "./LoadingPage.svelte";
    import MainPrompt from "./MainPrompt.svelte";
    import Splash from "./Splash.svelte";
    import LessonModal from "./LessonModal.svelte";

    import { currentPageTrigger } from "./customStore.js";
    import Sidebar from "./Sidebar.svelte";

    let currPage = "splash";

    currentPageTrigger.subscribe((page) => {
        if (page != null) currPage = page;
    });
</script>

<main>
    <Sidebar />
    {#if currPage === "splash"}
        <Splash />
    {/if}
    {#if currPage === "loading"}
        <LoadingPage />
    {/if}
    {#if currPage === "main" || currPage === "loading"}
        <div class:hidden={currPage != "main"} class="main-page">
            <CoverPage />
            <MainPrompt />
        </div>
    {/if}
</main>

<style>
    main {
        /* border-style: solid; */
        height: 97vh;
        width: 100%;
    }
    .hidden {
        display: none;
    }
    .main-page {
        margin-bottom: 20vh;
    }
</style>
