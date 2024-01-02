from llm import prompt_llm
import yaml
import json
import time

def fake_stream(text, delay=0.01):
    for char in text:
        yield char
        time.sleep(delay)

def generate_lesson(lesson, syllabus):
#     response_text = f"""In measure theory, an area of mathematics, Egorov's theorem establishes a condition for the uniform convergence of a pointwise convergent sequence of measurable functions. It is also named Severini–Egoroff theorem or Severini–Egorov theorem, after Carlo Severini, an Italian mathematician, and Dmitri Egorov, a Russian physicist and geometer, who published independent proofs respectively in 1910 and 1911.

# Egorov's theorem can be used along with compactly supported continuous functions to prove Lusin's theorem for integrable functions.
# Historical note
# The first proof of the theorem was given by Carlo Severini in 1910:[1][2] he used the result as a tool in his research on series of orthogonal functions. His work remained apparently unnoticed outside Italy, probably due to the fact that it is written in Italian, appeared in a scientific journal with limited diffusion and was considered only as a means to obtain other theorems. A year later Dmitri Egorov published his independently proved results,[3] and the theorem became widely known under his name: however, it is not uncommon to find references to this theorem as the Severini–Egoroff theorem. The first mathematicians to prove independently the theorem in the nowadays common abstract measure space setting were Frigyes Riesz (1922, 1928), and in Wacław Sierpiński (1928):[4] an earlier generalization is due to Nikolai Luzin, who succeeded in slightly relaxing the requirement of finiteness of measure of the domain of convergence of the pointwise converging functions in the ample paper (Luzin 1916).[5] Further generalizations were given much later by Pavel Korovkin, in the paper (Korovkin 1947), and by Gabriel Mokobodzki in the paper (Mokobodzki 1970). """
#     for output in fake_stream(response_text):
#         yield output
#     return

    prompt = f"""
Generate a short introductory lesson on the given subject.
Aim for roughly 200 words.

Syllabus: syllabus
Lesson: TuringMachines

  <h1>Understanding Turing Machines</h1>
    <p>A <strong>Turing Machine</strong> is a fundamental concept in the field of computer science and computational theory, conceptualized by the mathematician Alan Turing in 1936. It's a theoretical device that manipulates symbols on a strip of tape according to a set of rules. Despite its simplicity, a Turing Machine can be adapted to simulate the logic of any computer algorithm, and is thus powerful enough to model the computation of any data manipulable by a computer.</p>
    
    <h2>Components of a Turing Machine</h2>
    <ul>
        <li><strong>Tape:</strong> Divided into discrete cells, each of which can contain a symbol. The tape is usually considered infinitely long, allowing for unlimited computation.</li>
        <li><strong>Head:</strong> Reads and writes symbols on the tape and can move the tape left and right one cell at a time.</li>
        <li><strong>State Register:</strong> Stores the state of the Turing Machine. The number of states is finite and one state is designated as the start state.</li>
        <li><strong>Table of Instructions:</strong> Dictates the machine's actions, based on the current state and the symbol it reads on the tape.</li>
    </ul>

    <h2>Functioning of a Turing Machine</h2>
    <p>A Turing Machine operates based on its instruction table. For a given state and a symbol read by the head, the machine will write a new symbol in the cell, move the head left or right, and transition to a new state. This process continues until the machine reaches a halting state, where no further actions are defined.</p>

    <h2>Significance</h2>
    <p>The concept of Turing Machines is crucial in the theory of computation, as it helps in understanding what can (or cannot) be computed. It's a cornerstone in discussions about the limits of computational power and decidability.</p>

Syllabus: {syllabus}
Lesson: {lesson}
"""
    
    for chunk in prompt_llm(prompt):
        yield chunk


def generate_tree(chapters):
    prompt = f"""

Put the chapters of the syllabus into a tree to represent possible learning paths.
Each edge represents a prerequisite between two chapters.
For each chapter, output the prerequisite for that chapter. If a chapter has no prerequisites, represent this with an empty list.
A chapter can only have the chapters defined before it as prerequisites, that is, the chapters must be topologically sorted.
Only output the immediate prerequisites to avoid redundancy.

Don't let the order that the chapters are presented influence your tree.
Come up with your own order based on your intuition of how much each chapter builds upon previous chapters.
For each chapter, a few lessons are listed to give you a better sense of the chapter contents.

Output your tree as a DAG using the following yaml format:

ChaptersTree:
    "chapter A": []
    "chapter B": []
    "chapter C":
        - "chapter B"
    "chapter D":
        - "chapter A"
        - "chapter C"

(1/3)
Chapters:
    Regular Languages:
        - Finite Automata
        - Regular Expressions
        - Nonregular Languages
    Context-Free Languages:
        - Context-Free Grammars
        - Pushdown Automata
        - Non-Context-Free Languages
    The Church-Turing Thesis:
        - Turing Machines
        - Variants of Turing Machines
        - The Definition of Algorithm
    Decidability:
        - Decidable Languages
        - Undecidability
    Reducibility:
        - Undecidable Problems from Language Theory
        - Mapping Reducibility
    Advanced Topics in Computability Theory:
        - The Recusion Theorem
        - Decidability of Logical Theories
    Time Complexity:
        - Measuring Complexity
        - The Class P
        - The Class NP
        - NP-completeness
    Space Complexity:
        - Savitch's Theorem
        - The Class PSPACE
        - PSPACE-completeness
        - The Classes L and NL
        - NL-completeness
    Intractability:
        - Hierarchy Theorems
        - Relativization
        - Circuit Complexity

ChaptersTree:
    "Regular Languages": []
    "Context-Free Languages":
        - "Regular Languages"
    "The Church-Turing Thesis":
        - "Context-Free Languages"
    "Decidability":
        - "The Church-Turing Thesis"
    "Reducibility":
        - "Decidability"
    "Time Complexity":
        - "The Church-Turing Thesis"
    "Space Complexity":
        - "Time Complexity"
    "Intractability":
        - "Time Complexity"
        - "Space Complexity"
    "Advanced Topics in Computability Theory":
        - "Reducibility"
        - "Intractability"

(2/3)
Chapters:
    Introduction to Machine Learning:
        - Overview of Machine Learning
        - Types of Machine Learning
        - Evaluation Metrics
    Data Preprocessing:
        - Data Cleaning
        - Feature Selection and Extraction
        - Data Transformation Techniques
    Regression Analysis:
        - Linear Regression
        - Polynomial Regression
        - Regularization Methods
    Classification Techniques:
        - Decision Trees
        - Nearest Neighbour Methods
        - Support Vector Machines
        - Neural Networks
    Model Evaluation:
        - Cross-Validation
        - Overfitting and Underfitting
        - Performance Metrics
    Clustering:
        - K-Means Clustering
        - Hierarchical Clustering
        - Density-Based Clustering
    Dimensionality Reduction:
        - Principal Component Analysis
        - Autoencoders
        - t-SNE and UMAP

ChaptersTree:
    "Introduction to Machine Learning": []
    "Data Preprocessing": []
    "Regression Analysis":
        - "Introduction to Machine Learning"
        - "Data Preprocessing"
    "Classification Techniques":
        - "Regression Analysis"
    "Model Evaluation":
        - "Regression Analysis"
    "Clustering":
        - "Introduction to Machine Learning"
        - "Data Preprocessing"
    "Dimensionality Reduction":
        - "Model Evaluation"
        - "Clustering"

(3/3)
Chapters:
{chapters}

"""
    response_text = ""
    for chunk in prompt_llm(prompt):
        response_text += chunk
        if "Chapters:" in response_text: # don't generate more few shot
            print("EARLY END")
            return chunk
        yield chunk

def generate_syllabus(course):
    prompt = f"""
Create a syllabus on the following prompts. Additionally generate a course title and description. 
Unless otherwise specified, assume the course is at an introductory level.
There should be 2-4 units.
Each unit should have 2-4 chapters.
Each chapter should have 2-5 lessons.
Try to have at least 8-9 chapters.

Make sure to format the syllabus in yaml EXACTLY as follows:
Syllabus:
- "Unit 1: _":
    - "Chapter 1: _":
        - "Lesson 1.1: _"
        - "Lesson 1.2: _"
    - "Chapter 2: _":
        - "Lesson 2.1: _"
- "Unit 2: _":
    - "Chapter 3: _":
        - "Lesson 3.1: _"

(1/3)
Prompt: "computational complexity"
Course: "Introduction to Computational Complexity and Computability"
Description: "Introduction to the theory of computability: Turing machines and other models of computation, Church’s thesis, computable and noncomputable functions, recursive and recursively enumerable sets, many-one reductions. Introduction to complexity theory: P, NP, polynomial time reducibility, NP-completeness, self-reducibility, space complexity (L, NL, PSPACE and completeness for those classes), hierarchy theorems, and provably intractable problems."
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
          - "Lesson 6.1: The Recursion Theorem"
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

(2/3)
Prompt: "machine learning"
Course: "Introduction to Machine Learning"
Description: "An introduction to methods for automated learning of relationships on the basis of empirical data. Classification and regression using nearest neighbour methods, decision trees, linear models, and neural networks. Clustering algorithms. Problems of overfitting and of assessing accuracy."
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

(3/3)
Prompt: "{course}"
"""

    for chunk in prompt_llm(prompt):
        yield chunk

def generate_chapter_intro(chapter, syllabus):
    prompt = f"""
{syllabus}

Write a 140 word introduction to the chapter "{chapter}".
"""
    for chunk in prompt_llm(prompt):
        yield chunk

def generate_course_intro(course, syllabus):
    prompt = f"""
Generate a 100-150 word introduction to the following courses. 
Write one introductory sentence, one sentence for each unit, and one concluding sentence.
Be sure to begin your response with `Introduction: `. Do not wrap your text in quotes.
Please format your text with each sentence on a new line.
First is an example (1/2), followed by your prompt (2/2).

(1/2)
Course: Introduction to Machine Learning
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
Introduction: Welcome to "Exploring the Depths of Real Analysis," a course meticulously crafted to navigate the complex world of real analysis.
In Unit 1, we establish foundational knowledge, delving into sets, numbers, sequences, and series, focusing on their properties and convergence.
Unit 2 shifts to Limits and Continuity, exploring the nuanced definitions and properties of limits, alongside the pivotal Intermediate Value Theorem.
Unit 3, covering Differentiation and Integration, addresses core calculus principles, from derivative concepts to the Fundamental Theorem of Calculus and integration techniques.
The course culminates in Unit 4 with Advanced Topics, introducing sequences and series of functions, metric spaces, and Lebesgue Integration.
This course is an ideal journey for those seeking a profound understanding of real analysis, blending theoretical depth with practical insights.

(2/2)
Course: {course}
Syllabus:
{syllabus}
    """

    for chunk in prompt_llm(prompt):
        yield chunk

def parse_tree(llm_output):
    tree = yaml.safe_load(llm_output)

    nodes = []
    edges = []

    for lesson, prerequisites in tree['LessonTree'].items():
        nodes.append({'data': {'id': lesson, 'label': lesson}})

        for prereq in prerequisites:
            edges.append({'data': {'source': prereq, 'target': lesson}})

    tree_json = json.dumps({
        'nodes': nodes,
        'edges': edges
    }, indent=4)

    return tree_json


if __name__ == "__main__":
    for v in generate_tree("piano"):
        pass