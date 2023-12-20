<script>
    import PromptBox from "./PromptBox.svelte";

</script>
<main>
    <div class="title-box">
        <div class="title">
        branching <br> factor
        </div>
        <div class="title-sub">
            Free is the puppet the who loves their strings. <br> In what way are <i><b>you</b></i> free?
        </div>
        <PromptBox />
 </div>
    <!-- <div class="tree"> -->
        <img src="tree.jpg" class="tree"/>
    <!-- </div> -->
</main>

<style>
    main {
        /* border-style: solid; */
        overflow: hidden;
        height: 100%;
        width: 100%;
        display: flex;
    }
    .title-box {
        /* border-style: solid;
        border-color: red; */
        top: 50%;
        padding-left: 35px;
        position: relative;
    }
    .title {
        font-family: sans-serif;
        font-size: 100px;
    }
    .title-sub {
        font-family: sans-serif;
        font-size: 40px;
    }
    .tree {
        position: absolute;

        height: 150vh;
        width: auto;
        bottom: 1px;
        right: 0;
        z-index: -1;
    }
</style>
