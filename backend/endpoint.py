import time
from flask import Flask, Response, stream_with_context, request, jsonify
from flask_cors import CORS
from prompts import generate_tree, generate_lesson

app = Flask(__name__)
CORS(app)

@app.route('/generate_tree')
def generate_endpoint():
    def generate_stream(prompt):
        print("Generating tree for prompt:", prompt)
        for output in generate_tree(prompt):
            yield output
        yield "\n\n"

    prompt = request.args.get('prompt')

    # Check if the prompt is provided and is not just whitespace
    if not prompt or prompt.strip() == "":
        return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(generate_stream(prompt)), mimetype='text/plain')

@app.route('/generate_lesson')
def generate_lesson_endpoint():
    def generate_stream(prompt):
        print("Generating lesson for prompt:", prompt)
        for output in generate_lesson(prompt):
            yield output
        yield "\n\n"

    prompt = request.args.get('prompt')

    # Check if the prompt is provided and is not just whitespace
    if not prompt or prompt.strip() == "":
        return jsonify({"error": "No valid prompt provided"}), 400

    return Response(stream_with_context(generate_stream(prompt)), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
