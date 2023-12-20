<script>

import { splashPromptTrigger } from './customStore.js';

let promptText = "machine learning";

function handleClick() {
    splashPromptTrigger.broadcast(promptText);
}



</script>

<main>
    <div>
        <input bind:value={promptText} type="text"/>
        <button on:click={handleClick} >???</button>
    </div>
</main>

<style>
input, button {
    margin: 0;
    padding: 0;
    border: none;
    background: none;
}

input[type="text"] {
    width: 400px;
    padding: 10px;
    border: 2px solid black;
    background-color: #f0f0f0;
    color: black;
    font-size: 30px;
    box-shadow: 5px 5px 0px #000;
    margin: 10px;
    outline: none;
}

button {
    padding: 10px 20px;
    border: 2px solid black;
    background-color: rgb(176, 240, 176);
    font-size: 30px;
    text-transform: uppercase;
    cursor: pointer;
    box-shadow: 5px 5px 0px #000;
    margin: 10px;
}

button:hover {
    background-color: rgb(216, 236, 216);
}

</style>