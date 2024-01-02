<script>
    import { onMount } from "svelte";
    import { fade } from 'svelte/transition';3
    import { courseObjectTrigger } from "./customStore";
    import yaml from "js-yaml";
    export let title = "";
    export let intro = "";
    export let syllabusText = "";

//     title = "Introduction to Real Analysis";
//     syllabusText = `
//     - "Unit 1: Foundations of Real Analysis":
//     - "Chapter 1: Sets and Numbers":
//         - "Lesson 1.1: Sets and Operations"
//         - "Lesson 1.2: Ordered Sets"
//         - "Lesson 1.3: The Real Number System"
//     - "Chapter 2: Sequences":
//         - "Lesson 2.1: Convergence of Sequences"
//         - "Lesson 2.2: Subsequences"
//         - "Lesson 2.3: Bounded and Monotone Sequences"
//     - "Chapter 3: Series":
//         - "Lesson 3.1: Convergence of Series"
//         - "Lesson 3.2: Tests for Convergence"
//         - "Lesson 3.3: Power Series"
// - "Unit 2: Limits and Continuity":
//     - "Chapter 4: Limits":
//         - "Lesson 4.1: Definition of Limits"
//         - "Lesson 4.2: Properties of Limits"
//         - "Lesson 4.3: One-Sided Limits"
//     - "Chapter 5: Continuity":
//         - "Lesson 5.1: Definition of Continuity"
//         - "Lesson 5.2: Properties of Continuous Functions"
//         - "Lesson 5.3: Intermediate Value Theorem"
// - "Unit 3: Differentiation and Integration":
//     - "Chapter 6: Differentiation":
//         - "Lesson 6.1: Definition of Derivatives"
//         - "Lesson 6.2: Differentiation Rules"
//         - "Lesson 6.3: Mean Value Theorem"
//     - "Chapter 7: Integration":
//         - "Lesson 7.1: Riemann Integrals"
//         - "Lesson 7.2: Fundamental Theorem of Calculus"
//         - "Lesson 7.3: Techniques of Integration"
//         - "Lesson 7.4: Improper Integrals"
// - "Unit 4: Advanced Topics in Real Analysis":
//     - "Chapter 8: Sequences and Series of Functions":
//         - "Lesson 8.1: Pointwise and Uniform Convergence"
//         - "Lesson 8.2: Continuity and Differentiability of Limit Functions"
//     - "Chapter 9: Metric Spaces":
//         - "Lesson 9.1: Definition and Examples of Metric Spaces"
//         - "Lesson 9.2: Open and Closed Sets"
//         - "Lesson 9.3: Completeness and Compactness"
//     - "Chapter 10: Introduction to Lebesgue Integration":
//         - "Lesson 10.1: Riemann vs Lebesgue Integrals"
//         - "Lesson 10.2: Measure Theory Basics"
//         - "Lesson 10.3: Lebesgue Integration of Bounded Functions"
    // `

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
        height: auto;
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
        font-size: min(80px, 8vw);
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
