<script>
    export let content;
    let preElement;
    function scrollToBottom() {
        if (preElement != null) {
            preElement.scrollTop = preElement.scrollHeight;
        }
    }

    // Call scrollToBottom whenever content changes
    $: if (content) {
        scrollToBottom();
    }
</script>

<main>
    <pre bind:this={preElement}>
    {content}
    </pre>
</main>

<style>
    pre {
        white-space: pre-wrap; /* CSS3 */
        white-space: -moz-pre-wrap; /* Firefox */
        white-space: -pre-wrap; /* Opera <7 */
        white-space: -o-pre-wrap; /* Opera 7 */
        word-wrap: break-word; /* Internet Explorer 5.5+ */

        height: 100%; /* Keep 100% height */
        overflow-y: hidden; /* Scrollbar only when necessary */
        overflow-x: hidden; /* Hide horizontal scrollbar */
        border: 2px solid black;
        padding: 10px;
        margin: 0; /* Remove default margin */
        box-sizing: border-box; /* Include padding and border in the element's total width and height */
        background-color: lightgray;
    }
    main {
        height: 100%; /* Keep 100% height */
        max-width: 100%;
        width: 100%;
        overflow: hidden; /* Hide overflow */
        position: relative; /* For proper height calculation */
    }
</style>
