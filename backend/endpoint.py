import time
from flask import Flask, Response, stream_with_context, request, jsonify
from flask_cors import CORS
from prompts import generate_tree, generate_lesson, generate_syllabus, generate_chapter_intro

app = Flask(__name__)
CORS(app)

@app.route('/generate_tree')
def generate_endpoint():
    response_text = """ChaptersTree:
    "Sets and Numbers": []
    "Sequences":
        - "Sets and Numbers"
    "Series":
        - "Sequences"
    "Limits":
        - "Sequences"
    "Continuity":
        - "Limits"
    "Differentiation":
        - "Continuity"
    "Integration":
        - "Differentiation"
        - "Series"
    "Sequences and Series of Functions":
        - "Sequences"
        - "Series"
    "Metric Spaces":
        - "Sequences"
        - "Continuity"
    "Introduction to Lebesgue Integration":
        - "Integration"
        - "Metric Spaces" """
    
    # return Response(response_text, mimetype='text/plain')

    def generate_stream(prompt):
        print("Generating tree for prompt:", prompt)
        for output in generate_tree(prompt):
            yield output
        yield "\n\n"

    prompt = request.args.get('prompt')

    if not prompt or prompt.strip() == "":
        return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(generate_stream(prompt)), mimetype='text/plain')

@app.route('/generate_lesson')
def generate_lesson_endpoint():
    def generate_stream(prompt, syllabus):
        print("Generating lesson for prompt:", prompt)
        for output in generate_lesson(prompt, syllabus):
            yield output
        yield "\n\n"

    prompt = request.args.get('prompt')
    syllabus = request.args.get('prompt', 'syllabus')

    if not prompt or prompt.strip() == "":
        return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(generate_stream(prompt, syllabus)), mimetype='text/plain')

@app.route('/generate_syllabus')
def generate_syllabus_endpoint():
    response_text = """Description: "An introductory course in real analysis, focusing on the properties and structures of real numbers, limits, continuity, and differentiability of functions, as well as sequences and series. Also covers the basics of integration and topics such as the intermediate value theorem, mean value theorem, and the Riemann integral."

Syllabus:
- "Unit 1: Foundations of Real Analysis":
    - "Chapter 1: Sets and Numbers":
        - "Lesson 1.1: Sets and Operations"
        - "Lesson 1.2: Ordered Sets"
        - "Lesson 1.3: The Real Number System"
    - "Chapter 2: Sequences":
        - "Lesson 2.1: Convergence of Sequences"
        - "Lesson 2.2: Subsequences"
        - "Lesson 2.3: Bounded and Monotone Sequences"
    - "Chapter 3: Series":
        - "Lesson 3.1: Convergence of Series"
        - "Lesson 3.2: Tests for Convergence"
        - "Lesson 3.3: Power Series"
- "Unit 2: Limits and Continuity":
    - "Chapter 4: Limits":
        - "Lesson 4.1: Definition of Limits"
        - "Lesson 4.2: Properties of Limits"
        - "Lesson 4.3: One-Sided Limits"
    - "Chapter 5: Continuity":
        - "Lesson 5.1: Definition of Continuity"
        - "Lesson 5.2: Properties of Continuous Functions"
        - "Lesson 5.3: Intermediate Value Theorem"
- "Unit 3: Differentiation and Integration":
    - "Chapter 6: Differentiation":
        - "Lesson 6.1: Definition of Derivatives"
        - "Lesson 6.2: Differentiation Rules"
        - "Lesson 6.3: Mean Value Theorem"
    - "Chapter 7: Integration":
        - "Lesson 7.1: Riemann Integrals"
        - "Lesson 7.2: Fundamental Theorem of Calculus"
        - "Lesson 7.3: Techniques of Integration"
        - "Lesson 7.4: Improper Integrals"
- "Unit 4: Advanced Topics in Real Analysis":
    - "Chapter 8: Sequences and Series of Functions":
        - "Lesson 8.1: Pointwise and Uniform Convergence"
        - "Lesson 8.2: Continuity and Differentiability of Limit Functions"
    - "Chapter 9: Metric Spaces":
        - "Lesson 9.1: Definition and Examples of Metric Spaces"
        - "Lesson 9.2: Open and Closed Sets"
        - "Lesson 9.3: Completeness and Compactness"
    - "Chapter 10: Introduction to Lebesgue Integration":
        - "Lesson 10.1: Riemann vs Lebesgue Integrals"
        - "Lesson 10.2: Measure Theory Basics"
        - "Lesson 10.3: Lebesgue Integration of Bounded Functions"
        """
    # return Response(response_text, mimetype='text/plain')
    def generate_stream(prompt):
        print("Generating syllabus for prompt:", prompt)
        for output in generate_syllabus(prompt):
            yield output
        yield "\n\n"

    prompt = request.args.get('prompt')

    if not prompt or prompt.strip() == "":
        return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(generate_stream(prompt)), mimetype='text/plain')

@app.route('/generate_chapter_intro')
def generate_chapter_endpoint():
    def generate_stream(chapter, syllabus):
        print("Generating chapter intro for prompt:", chapter, syllabus)
        for output in generate_chapter_intro(chapter, syllabus):
            yield output
        yield "\n\n"

    chapter = request.args.get('chapter')
    syllabus = request.args.get('syllabus')

    if not chapter or chapter.strip() == "":
        return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(generate_stream(chapter, syllabus)), mimetype='text/plain')
if __name__ == '__main__':
    app.run(debug=True)

