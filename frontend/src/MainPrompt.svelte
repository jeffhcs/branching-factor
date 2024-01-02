<script>
    import LessonTree from "./LessonTree.svelte";
    import yaml from "js-yaml";
    import ChapterLessonsPanel from "./ChapterLessonsPanel.svelte";
    import Syllabus from "./Syllabus.svelte";
    import {
        parseSyllabusYaml,
        getChaptersForTree,
    } from "./parsing/parseSyllabus";
    import { splashPromptTrigger, loadingTextTrigger, currentPageTrigger, courseObjectTrigger } from './customStore.js';

    let lessonTreeComponent;

    function parseToTreeElements(llmOutput, chaptersData) {
        const rootKey = "ChaptersTree";
        try {
            const newlineCount = (llmOutput.match(/\n/g) || []).length;
            if (newlineCount < 2) {
                return false;
            }

            var cleanedText = llmOutput;

            if (cleanedText.lastIndexOf("\n\n") > -1) {
                cleanedText = cleanedText.substring(
                    0,
                    cleanedText.lastIndexOf("\n\n"),
                );
            } else {
                cleanedText = cleanedText.substring(
                    0,
                    cleanedText.lastIndexOf("\n"),
                );
            }

            cleanedText.trimEnd();

            if (cleanedText.charAt(cleanedText.length - 1) === ":") {
                cleanedText = cleanedText.substring(
                    0,
                    cleanedText.lastIndexOf("\n"),
                );
            }

            const tree = yaml.load(cleanedText);

            const elements = [];

            for (const chapter in tree[rootKey]) {
                const prerequisites = tree[rootKey][chapter];

                elements.push({
                    group: "nodes",
                    data: { id: chapter, lessons: chaptersData[chapter] },
                });

                prerequisites.forEach((prereq) => {
                    elements.push({
                        group: "edges",
                        data: { source: prereq, target: chapter },
                    });
                });
            }

            return elements;
        } catch (e) {
            console.error(llmOutput, "|", cleanedText, e);
            return false;
        }
    }
    let generateTreeXhr = new XMLHttpRequest();
    function callGenerateTreeEndpoint(chaptersData) {
        generateTreeXhr.abort();
        generateTreeXhr = new XMLHttpRequest();
        generateTreeXhr.open(
            "GET",
            "http://127.0.0.1:5000/generate_tree?prompt=" +
                encodeURIComponent(yaml.dump(chaptersData)),
            true,
        );
        generateTreeXhr.onprogress = function () {
            const elements = parseToTreeElements(
                generateTreeXhr.responseText,
                chaptersData,
            );
            if (elements) lessonTreeComponent.update_tree(elements);
        };
        generateTreeXhr.send();
    }
    let generateSyllabusXhr = new XMLHttpRequest();
    function callGenerateSyllabusEndpoint(prompt) {
        generateSyllabusXhr.abort();
        generateSyllabusXhr = new XMLHttpRequest();
        generateSyllabusXhr.open(
            "GET",
            "http://127.0.0.1:5000/generate_syllabus?prompt=" +
                encodeURIComponent(prompt),
            true,
        );
        generateSyllabusXhr.onprogress = function () {
            // console.log(generateSyllabusXhr.responseText);
            // const elements = parseToTreeElements(generateTreeXhr.responseText);
            // if (elements) lessonTreeComponent.update_tree(elements);
            syllabusText = generateSyllabusXhr.responseText;
            loadingTextTrigger.broadcast(syllabusText);

        };
        generateSyllabusXhr.onreadystatechange = function () {
            if (generateSyllabusXhr.readyState === XMLHttpRequest.DONE) {
                if (generateSyllabusXhr.status === 200) {
                    syllabus = parseSyllabusYaml(syllabusText);
                    if (syllabus) {
                        currentPageTrigger.broadcast("main");
                        courseObjectTrigger.broadcast(syllabus);
                        const chaptersPrompt = getChaptersForTree(syllabus);
                        callGenerateTreeEndpoint(chaptersPrompt);
                        // lessonTreeComponent.update_tree(chapters);
                    }
                } else {
                    console.log("There was a problem with the request.");
                }
            }
        };
        currentPageTrigger.broadcast("loading");
        generateSyllabusXhr.send();
    }
    let courseNamePrompt = "";
    let syllabusText = "";
    let syllabus;

    function generate() {
        // callGenerateTreeEndpoint(courseNamePrompt);
        callGenerateSyllabusEndpoint(courseNamePrompt);
    }

    let selectedChapterData;

    function handleChapterClicked(event) {
        selectedChapterData = event.detail;
    }

    function handleClosePanel() {
        selectedChapterData = null;
    }

    splashPromptTrigger.subscribe((promptText) => {
        if (promptText != null) {
            courseNamePrompt = promptText;
            generate();
        }
    });
</script>

<main>
    <!-- <div>
        Where's Curiosity Taking You?
        <input type="text" bind:value={courseNamePrompt} />
        <button on:click={generate}>Generate</button>
    </div> -->
    <div class="tree-window">
        <div class="lesson-tree">
            <LessonTree
                bind:this={lessonTreeComponent}
                on:chapterClicked={handleChapterClicked}
            />
        </div>
        {#if selectedChapterData}
            <div class="chapter-panel">
                <ChapterLessonsPanel bind:chapterData={selectedChapterData} bind:syllabusText={syllabusText} on:closePanel={handleClosePanel}/>
            </div>
        {/if}
    </div>
    <!-- <Syllabus bind:content={syllabusText} /> -->
</main>

<style>
    main {
        font-family: "Arial", sans-serif;
        /* background-color: #f4f4f4; */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0;
        color: #333;
    }

    input[type="text"] {
        padding: 10px;
        margin: 10px 0;
        border: none;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    }

    button {
        padding: 10px 15px;
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        color: white;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #0056b3;
    }
    .tree-window {
        display: flex;
        /* justify-content: space-between; 
        align-items: start;  */
        border: black solid 3px;
        width: 80vw;
        height: 75vh;
    }

    .lesson-tree {
        flex-grow: 2;
        flex-basis: 0;
        flex-shrink: 1;
        overflow: hidden;
    }
    .chapter-panel {
        flex-grow: 1;
        flex-basis: 0;
        flex-shrink: 0;
    }
</style>
