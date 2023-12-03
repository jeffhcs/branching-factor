import yaml from 'js-yaml';

export function parseSyllabusYaml(yamlString) {
    try {
        const parsedYaml = yaml.load(yamlString);
        return parsedYaml;
    } catch (e) {
        console.error(e);
        return null;
    }
}

// Example usage:
const yamlString = `
Syllabus:
  - "Unit 1: Automata and Languages":
      - "Chapter 1: Regular Languages":
          - "Lesson 1.1: Finite Automata"
          - "Lesson 1.2: Regular Expressions"
          - "Lesson 1.3: Nonregular Languages"
      - "Chapter 2: Context-Free Languages":
          - "Lesson 2.1: Context-Free Grammars"
          - "Lesson 2.2: Pushdown Automata"
          - "Lesson 2.3: Non-Context-Free Languages"
  - "Unit 2: Computability Theory":
      - "Chapter 3: The Church-Turing Thesis":
          - "Lesson 3.1: Turing Machines"
          - "Lesson 3.2: Variants of Turing Machines"
          - "Lesson 3.3: The Definition of Algorithm"
      - "Chapter 4: Decidability":
          - "Lesson 4.1: Decidable Languages"
          - "Lesson 4.2: Undecidability"
      - "Chapter 5: Reducibility":
          - "Lesson 5.1: Undecidable Problems from Language Theory"
          - "Lesson 5.2: Mapping Reducibility"
      - "Chapter 6: Advanced Topics in Computability Theory":
          - "Lesson 6.1: The Recusion Theorem"
          - "Lesson 6.2: Decidability of Logical Theories"
  - "Unit 3: Complexity Theory":
      - "Chapter 7: Time Complexity":
          - "Lesson 7.1: Measuring Complexity"
          - "Lesson 7.2: The Class P"
          - "Lesson 7.3: The Class NP"
          - "Lesson 7.4: NP-completeness"
      - "Chapter 8: Space Complexity":
          - "Lesson 8.1: Savitch's Theorem"
          - "Lesson 8.2: The Class PSPACE"
          - "Lesson 8.3: PSPACE-completeness"
          - "Lesson 8.4: The Classes L and NL"
          - "Lesson 8.5: NL-completeness"
      - "Chapter 9: Intractability":
          - "Lesson 9.1: Hierarchy Theorems"
          - "Lesson 9.2: Relativization"
          - "Lesson 9.3: Circuit Complexity"
`;

const yamlML = `
Syllabus:
  - "Unit 1: Foundations of Machine Learning":
      - "Chapter 1: Introduction to Machine Learning":
          - "Lesson 1.1: Overview of Machine Learning"
          - "Lesson 1.2: Types of Machine Learning"
          - "Lesson 1.3: Evaluation Metrics"
      - "Chapter 2: Data Preprocessing":
          - "Lesson 2.1: Data Cleaning"
          - "Lesson 2.2: Feature Selection and Extraction"
          - "Lesson 2.3: Data Transformation Techniques"
  - "Unit 2: Supervised Learning":
      - "Chapter 3: Regression Analysis":
          - "Lesson 3.1: Linear Regression"
          - "Lesson 3.2: Polynomial Regression"
          - "Lesson 3.3: Regularization Methods"
      - "Chapter 4: Classification Techniques":
          - "Lesson 4.1: Decision Trees"
          - "Lesson 4.2: Nearest Neighbour Methods"
          - "Lesson 4.3: Support Vector Machines"
          - "Lesson 4.4: Neural Networks"
      - "Chapter 5: Model Evaluation":
          - "Lesson 5.1: Cross-Validation"
          - "Lesson 5.2: Overfitting and Underfitting"
          - "Lesson 5.3: Performance Metrics"
  - "Unit 3: Unsupervised Learning":
      - "Chapter 6: Clustering":
          - "Lesson 6.1: K-Means Clustering"
          - "Lesson 6.2: Hierarchical Clustering"
          - "Lesson 6.3: Density-Based Clustering"
      - "Chapter 7: Dimensionality Reduction":
          - "Lesson 7.1: Principal Component Analysis"
          - "Lesson 7.2: Autoencoders"
          - "Lesson 7.3: t-SNE and UMAP"
`

function removePrefixes(obj) {
    if (Array.isArray(obj)) {
        return obj.map(item => removePrefixes(item));
    } else if (typeof obj === 'string') {
        return obj.replace(/(Unit \d+: |Chapter \d+: |Lesson \d+\.\d+: )/g, '');
    } else if (typeof obj === 'object' && obj !== null) {
        const newObj = {};
        for (const key in obj) {
            newObj[removePrefixes(key)] = removePrefixes(obj[key]);
        }
        return newObj;
    }
    return obj;
}
function flattenChapters(data) {
    let flattened = {};

    // Iterate over each unit
    data.forEach(unit => {
        // Each unit is an object with a single key (the unit name) and an array of chapters
        for (const unitName in unit) {
            const chapters = unit[unitName];
            chapters.forEach(chapter => {
                // Each chapter is an object with a single key (the chapter name) and an array of lessons
                for (const chapterName in chapter) {
                    const lessons = chapter[chapterName];
                    // Assigning chapters as properties of the flattened object
                    flattened[chapterName] = lessons;
                }
            });
        }
    });

    return flattened;
}



export function getChaptersForTree(syllabus) {
    return flattenChapters(removePrefixes(syllabus)['Syllabus']);
}



function printObjJson(obj) {
    console.log(JSON.stringify(obj, null, 2));
}
function printObjYaml(obj) {
    console.log(yaml.dump(obj));
}


// const parsedData = parseSyllabusYaml(yamlString);
// const parsedDataWithoutPrefixes = removePrefixes(parsedData)['Syllabus'];
// const flattenedChapters = flattenChapters(parsedDataWithoutPrefixes);
// printObjYaml(flattenedChapters);
