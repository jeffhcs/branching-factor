<script>
    import { slide } from 'svelte/transition';
    import { currentPageTrigger, notebookTrigger } from './customStore';
    import { EndpointCaller } from "./backend.js";

    let sidebarOpen = false;

    let notebooks = []

    const notebooksEndpoint = new EndpointCaller("get_notebooks");
    notebooksEndpoint.onDone = (responseText) => {
        notebooks = JSON.parse(responseText);
    }

    $: if (sidebarOpen) {
        const access_token = JSON.parse(localStorage.getItem("oauth2-test-params"))["access_token"];
        notebooksEndpoint.call({access_token: access_token});
    }

    function openNotebook(notebookId) {
       currentPageTrigger.broadcast("main");
       notebookTrigger.broadcast(notebookId);
       sidebarOpen = false;
    }

</script>
<main>
    <div class="logo" on:click={()=>{sidebarOpen=true}}>
        Branching <br /> Factor
    </div>
    {#if sidebarOpen}
        <div class="sidebar" transition:slide={{ duration: 300, delay: 0, axis: 'x'}}>
            <span id="closeModal" class="close" on:click={()=>{sidebarOpen=false}}>&times;</span>
            <div class="menu" on:click={()=>{currentPageTrigger.broadcast("splash"); sidebarOpen=false;}}>Home</div>
            <div class="menu">Explore</div>
            <div class="menu">Customize</div>
            <div class="divider"/>
            <div class="heading">My Notebooks:</div>

            {#if notebooks.length == 0}
                <div class="notebook">No notebooks found.</div>
            {:else}
                {#each notebooks as notebook}
                    <div class="notebook" on:click={()=>{openNotebook(notebook.id)}}>{notebook.title}</div>
                {/each}
            {/if}
        </div>
    {/if}
</main>

<style>
    main {
        position: fixed;
        left: 0;
        top: 0;
        z-index: 1;
    }
    .logo {
        font-family: sans-serif;
        font-size: 20px;
        font-weight: bold;
        padding: 20px;
        cursor: pointer;
    }
    .logo:hover {
        text-decoration: underline;
    }
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: min(300px, 100vw);
        height: 100vh;
        padding: 20px;
        color: white;
        font-family: sans-serif;
        background-color: black;
        display: flex;
        flex-direction: column;
    }

    .close {
        color: white;
        text-align: right;
        font-size: 28px;
        font-weight: bold;
    }
    .close:hover,
    .close:focus {
        color: grey;
        text-decoration: none;
        cursor: pointer;
    }
    .divider {
        border-bottom: 1px solid white;
        margin: 20px 0;
    }
    .menu {
        /* padding: 20px 0; */
        cursor: pointer;
        font-size: 30px;
        line-height: 50px;
    }
    .menu:hover {
        text-decoration: underline;
        color: grey;
    }
    .heading {
        font-size: 20px;
        margin-bottom: 20px;
    }
    .notebook {
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 16px;
        line-height: 30px;
    }
    .notebook:hover {
        text-decoration: underline;
        color: grey;
    }
</style>
