import time
from flask import Flask, Response, stream_with_context, request, jsonify
from flask_cors import CORS
from prompts import generate_tree, generate_lesson, generate_syllabus, generate_chapter_intro, generate_course_intro
from generation import *
import threading
import json

app = Flask(__name__)
CORS(app)

def long_running_task():
    while True:
        # Replace this with the actual work you need to do
        print("Working...")
        time.sleep(1)  # Simulate work with a sleep

@app.route('/start_worker')
def start_worker():
    thread = threading.Thread(target=long_running_task)
    thread.daemon = True  # Set as a daemon so it will be killed once the main thread is dead
    thread.start()
    return "Worker started!"

@app.route('/get_tree')
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

    # def generate_stream(prompt):
    #     for output in getTree(prompt):
    #         yield output
    #     yield "\n\n"

    notebook_id = request.args.get('notebook_id')

    # if not prompt or prompt.strip() == "":
    #     return jsonify({"error": "No valid prompt provided"}), 400

    # return Response(get_tree(notebook_id), mimetype='text/plain')
    # return 
    response = get_tree(notebook_id)

    return response

@app.route('/get_lesson')
def generate_lesson_endpoint():

    notebook_id = request.args.get('notebook_id')
    unit_index = int(request.args.get('unit_index'))
    chapter_index = int(request.args.get('chapter_index'))
    lesson_index = int(request.args.get('lesson_index'))

    return Response(stream_with_context(get_lesson_content(notebook_id, unit_index, chapter_index, lesson_index)), mimetype='text/plain')

@app.route('/create_notebook')
def generate_syllabus_endpoint():

    # def generate_stream(prompt):
    #     print("Generating syllabus for prompt:", prompt)
    #     for output in generate_syllabus(prompt):
    #         yield output
    #     yield "\n\n"

    prompt = request.args.get('prompt')

    if not prompt or prompt.strip() == "":
        return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(create_notebook(prompt)), mimetype='text/plain')

@app.route('/get_notebook_cover')
def get_notebook_cover_endpoint():
    notebook_id = request.args.get('notebook_id')

    # if not prompt or prompt.strip() == "":
    #     return jsonify({"error": "No valid prompt provided"}), 400

    return jsonify(get_notebook_cover(notebook_id))


@app.route('/get_chapter_intro')
def generate_chapter_endpoint():

    notebook_id = request.args.get('notebook_id')
    unit_index = int(request.args.get('unit_index'))
    chapter_index = int(request.args.get('chapter_index'))

    return Response(stream_with_context(get_chapter_intro(notebook_id, unit_index, chapter_index)), mimetype='text/plain')

@app.route('/generate_intro')
def generate_intro_endpoint():
    def generate_stream(title, syllabus):
        print("Generating intro for prompt:", title, syllabus)
        for output in generate_course_intro(title, syllabus):
            yield output
        yield "\n\n"

    title = request.args.get('title')
    syllabus = request.args.get('syllabus')

    # if not chapter or chapter.strip() == "":
    #     return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(generate_stream(title, syllabus)), mimetype='text/plain')
if __name__ == '__main__':
    app.run(debug=True)

