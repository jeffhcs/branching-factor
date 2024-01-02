<script>
    import { splashPromptTrigger, currentPageTrigger } from "./customStore.js";

    let promptText = "";

    function handleClick() {
        splashPromptTrigger.broadcast(promptText);
        currentPageTrigger.broadcast("loading");
    }

    let texts = [
        "machine learning",
        "digital art",
        "philosophy of the mind",
        "quantum mechanics",
        "real analysis",
        "linguistics",
        "music theory",
        "microeconomics",
    ];
    let displayText = "";
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let isFocused = false;
    let typingSpeed = 50;
    let paused = false;

    function typeText() {
        if (paused) {
            typingSpeed = 1000;
            paused = false;
        } else {
            if (isFocused) return;

            let currentText = texts[textIndex];

            if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                paused = true;
            }

            if (isDeleting) {
                typingSpeed = 30;
                displayText = currentText.slice(0, charIndex);
                charIndex --;
            } else {
                typingSpeed = 60;
                displayText = currentText.slice(0, charIndex);
                charIndex ++;
            }
            if (charIndex === currentText.length + 1) {
                isDeleting = true;
                paused = true;
            }

        }
        setTimeout(typeText, typingSpeed);
    }

    function onFocus() {
        isFocused = true;
        displayText = "";
    }

    function onBlur() {
        isFocused = false;
        charIndex = 0;
        isDeleting = false;
        typeText();
    }

    // Start the typing effect
    typeText();
</script>

<main>
    <div>
        <input
            placeholder={displayText}
            bind:value={promptText}
            on:focus={onFocus}
            on:blur={onBlur}
            type="text"
        />
        <button on:click={handleClick}>→</button>
    </div>
</main>

<style>
    input,
    button {
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
