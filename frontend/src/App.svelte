<script>
    import CoverPage from "./CoverPage.svelte";
    import LoadingPage from "./LoadingPage.svelte";
    import MainPrompt from "./MainPrompt.svelte";
    import Splash from "./Splash.svelte";
    import LessonModal from "./LessonModal.svelte";
    import Login from "./Login.svelte";

    import { currentPageTrigger, notebookTrigger } from "./customStore.js";
    import Sidebar from "./Sidebar.svelte";

    let currPage = "splash";
    let notebook_id;

    currentPageTrigger.subscribe((page) => {
        if (page != null) currPage = page;
    });
    notebookTrigger.subscribe((nb) => {
        if (nb != null) notebook_id = nb;
    });
</script>

<main>
    <Sidebar />
    <Login />
    {#if currPage === "splash"}
        <Splash />
    {/if}
    {#if currPage === "loading"}
        <LoadingPage />
    {/if}
    {#if currPage === "main"}
        <CoverPage bind:notebook_id/>
        <MainPrompt bind:notebook_id/>
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
