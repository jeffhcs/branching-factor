<script>
    import { onMount } from "svelte";
    import { fade } from 'svelte/transition';3
    import { courseObjectTrigger } from "./customStore";
    import yaml from "js-yaml";
    export let title = "";
    export let intro = "";
    export let syllabusText = "";

//     title = "Introduction to Real Analysis";
//     intro = `
// Focuses on the core ideas and concepts of game theory and on applications of them in economics and other social sciences. Topics may include: oligopoly, electoral competition, the theory of public goods, voting theory, the free rider problem, repeated interaction, bargaining, evolutionary equilibrium, matching and auctions.
// How can we make collective decisions fairly? What does it mean to properly balance conflicting interests? How can we combine the well-being of individuals into a concept of societal well-being? We explore these and related ethical questions from the perspective of economic theory. A central tool is the axiomatic approach, which calls for decisions to be consistent, in precise senses, across related situations. Possible topics include: rationing problems, the Shapley value, fair division, discrimination, voting theory, foundations of utilitarianism and egalitarianism, measurement of inequality, population ethics, intergenerational equity, and concepts of equal opportunity.
//     `

    courseObjectTrigger.subscribe((course) => {
        if (course != null) {
            title = course.Course;
            syllabusText = yaml.dump(course.Syllabus, {quotingType: '"'});
            callGenerateIntroEndpoint(title, syllabusText);
        }
    });

    let generateIntroXhr = new XMLHttpRequest();

    function callGenerateIntroEndpoint(title, syllabus) {
        generateIntroXhr.abort();
        generateIntroXhr = new XMLHttpRequest();
        generateIntroXhr.open(
            "GET",
            "http://127.0.0.1:5000/generate_intro?title=" +
                encodeURIComponent(title) +
                "&syllabus=" +
                encodeURIComponent(syllabus),
            true,
        );
        generateIntroXhr.onprogress = function () {
            const raw_text = generateIntroXhr.responseText;
            const flag = "Introduction: "
            if (raw_text.slice(0, flag.length) === flag) {
                intro = raw_text.slice(flag.length)
            }
        };
        generateIntroXhr.send();
    }

    function scroll() {
        window.scrollBy({
            top: window.innerHeight, // Scroll down by one viewport height
            behavior: "smooth", // Enable smooth scrolling
        });
    }
    let scrollTop = 0;

    // Function to update the scroll position
    function updateScroll() {
        scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    }

    onMount(() => {
        // Attach the event listener on mount
        window.addEventListener("scroll", updateScroll);

        // Clean up the event listener on component destroy
        return () => {
            window.removeEventListener("scroll", updateScroll);
        };
    });
</script>

<main>
    <div class="cover-page">
        <img src="cover2.png" alt="Cover Image" class="cover-image" />
        <div class="content">
            <div class="title">{title}</div>

            {#each intro.split("\n") as line}
                <p>{line}</p>
            {/each}
        </div>
    </div>
    {#if scrollTop === 0}
    <a class="scroll-down" out:fade={{ duration: 200 }} on:click={scroll}>↓</a>
    {/if}
</main>

<style>
    .scroll-down {
        /* position: relative; */
        /* left: 50%;
  transform: translateX(-50%); */
        font-size: 40px;
        text-decoration: none;
    }
    .scroll-down:hover {
        color: #555; /* Change the color on hover */
        transform: translateX(1px) scale(1.1); /* Slightly enlarge the icon */
        cursor: pointer;
    }

    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-family: sans-serif;
        min-height: 100vh; /* Set the height to 100% of the viewport height */
        height: auto;
        /* margin-bottom: 10vh; */
    }
    .cover-page {
        display: flex;
        height: 100%;
        width: 80vw;
        justify-content: center; /* Center children horizontally */
        align-items: center; /* Center children vertically */
        margin-top: 10vh;
        margin-bottom: 5vh;
        /* padding-top: 5vh; */
        /* padding-bottom: 5vh; */
    }

    .cover-image {
        max-width: 40vw;
        max-height: 75vh;
        /* height: auto; */
        object-fit: cover;
    }

    .content {
        padding-left: 20px;
        padding-right: 40px;
        flex-grow: 1; /* Take up the remaining space */
        display: flex;
        flex-direction: column;
        justify-content: center; /* Vertically center the content */
    }

    .title,
    p {
        margin: 0;
    }

    .title {
        font-size: min(60px, 8vw);
        font-weight: bold;
        margin-bottom: 10px;
    }

    p {
        font-size: 18px;
        text-align: justify;
    }
    p:not(:first-of-type) {
        text-indent: 40px; /* Adjust the indent size as needed */
    }
    /* Media query for narrow viewports */
    @media (max-width: 1200px) {
        .cover-page {
            flex-direction: column; /* Stack elements vertically */
        }
        .cover-image {
            max-width: 100%;
        }
        .content {
            padding-top: 20px;
            justify-content: flex-start;
        }
        .scroll-down {
            display: none;
        }
    }
</style>
