import time
from flask import Flask, Response, stream_with_context, request, jsonify
from flask_cors import CORS
from prompts import generate_tree, generate_lesson, generate_syllabus, generate_chapter_intro, generate_course_intro

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
    response_text = """Course: "Advanced Topics in Machine Learning"
Description: "An in-depth exploration of advanced techniques and algorithms in machine learning. Topics include deep learning, reinforcement learning, natural language processing, and recommendation systems. Students will gain hands-on experience through programming assignments and projects."
Syllabus:
  - "Unit 1: Deep Learning":
      - "Chapter 1: Neural Networks":
          - "Lesson 1.1: Introduction to Neural Networks"
          - "Lesson 1.2: Activation Functions"
          - "Lesson 1.3: Backpropagation"
      - "Chapter 2: Convolutional Neural Networks":
          - "Lesson 2.1: Convolutional Layers and Pooling"
          - "Lesson 2.2: Regularization Techniques"
          - "Lesson 2.3: Transfer Learning"
      - "Chapter 3: Recurrent Neural Networks":
          - "Lesson 3.1: LSTM and GRU Networks"
          - "Lesson 3.2: Sequence-to-Sequence Models"
          - "Lesson 3.3: Attention Mechanisms"
  - "Unit 2: Reinforcement Learning":
      - "Chapter 4: Markov Decision Processes":
          - "Lesson 4.1: Introduction to Reinforcement Learning"
          - "Lesson 4.2: Markov Decision Processes"
          - "Lesson 4.3: Value Iteration and Policy Iteration"
      - "Chapter 5: Q-Learning":
          - "Lesson 5.1: Introduction to Q-Learning"
          - "Lesson 5.2: Temporal Difference Learning"
          - "Lesson 5.3: Exploration and Exploitation"
      - "Chapter 6: Policy Gradient Methods":
          - "Lesson 6.1: Policy Gradients and REINFORCE"
          - "Lesson 6.2: Advantage Actor-Critic Methods"
          - "Lesson 6.3: Proximal Policy Optimization"
  - "Unit 3: Natural Language Processing":
      - "Chapter 7: Text Processing":
          - "Lesson 7.1: Tokenization and Lemmatization"
          - "Lesson 7.2: Word Embeddings"
          - "Lesson 7.3: Language Models and Text Generation"
      - "Chapter 8: Sentiment Analysis":
          - "Lesson 8.1: Bag-of-Words Models"
          - "Lesson 8.2: Sentiment Analysis using Deep Learning"
          - "Lesson 8.3: Named Entity Recognition"
      - "Chapter 9: Machine Translation":
          - "Lesson 9.1: Sequence-to-Sequence Models for Machine Translation"
          - "Lesson 9.2: Attention-Based Models"
  - "Unit 4: Recommendation Systems":
      - "Chapter 10: Collaborative Filtering":
          - "Lesson 10.1: User-Based Collaborative Filtering"
          - "Lesson 10.2: Item-Based Collaborative Filtering"
      - "Chapter 11: Content-Based Filtering":
          - "Lesson 11.1: Content-Based Recommendation"
          - "Lesson 11.2: Nearest Neighbor Methods for Content-Based Filtering"
      - "Chapter 12: Hybrid Recommender Systems":
          - "Lesson 12.1: Combining Collaborative Filtering and Content-Based Filtering"
          - "Lesson 12.2: Model-Based Hybrid Recommender Systems"

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

