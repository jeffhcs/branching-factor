from llm import prompt_llm
import yaml
import json

def generate_lesson(subject):

    prompt = f"""
Generate a short introductory lesson on the given subject.
Aim for roughly 200 words.

Subject: TuringMachines

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

Subject: {subject}
"""
    
    for chunk in prompt_llm(prompt):
        yield chunk


def generate_tree(subject):
    few_shot = f"""
Subject: introduction to machine learning
LessonTree:
    FundamentalsOfSupervisedLearning: []

    BasicStatistics:
        - FundamentalsOfSupervisedLearning

    DataPreprocessing:
        - FundamentalsOfSupervisedLearning

    LinearRegression:
        - BasicStatistics
        - DataPreprocessing

    LogisticRegression:
        - BasicStatistics
        - DataPreprocessing

    DecisionTrees:
        - DataPreprocessing

    ModelEvaluationBasics:
        - LinearRegression
        - LogisticRegression
        - DecisionTrees

    EnsembleMethods:
        - DecisionTrees

    RandomForests:
        - EnsembleMethods

    GradientBoosting:
        - EnsembleMethods

    SupportVectorMachines:
        - BasicStatistics
        - DataPreprocessing

    NeuralNetworksBasics:
        - BasicStatistics
        - DataPreprocessing

    HyperparameterTuning:
        - ModelEvaluationBasics
        - RandomForests
        - GradientBoosting
        - SupportVectorMachines
        - NeuralNetworksBasics

Subject: complex analysis
LessonTree:
    ComplexNumbers: []

    ComplexFunctions:
        - ComplexNumbers

    ComplexDifferentiation:
        - ComplexFunctions

    ContourIntegration:
        - ComplexFunctions

    ResidueTheorem:
        - ComplexFunctions
        - ContourIntegration

    TaylorSeries:
        - ComplexFunctions

    LaurentSeries:
        - ComplexFunctions

    AnalyticFunctions:
        - ComplexDifferentiation
        - TaylorSeries

    CauchyRiemannEquations:
        - ComplexDifferentiation

    CauchyIntegralFormula:
        - AnalyticFunctions
        - ComplexDifferentiation

    ConformalMappings:
        - CauchyIntegralFormula
        - AnalyticFunctions

    HarmonicFunctions:
        - CauchyRiemannEquations

    ComplexIntegration:
        - ContourIntegration
        - ResidueTheorem

    SingularityClassification:
        - LaurentSeries
        - ResidueTheorem
"""

    prompt = f"""
Generate a lesson tree on the given subject with 10-12 lessons.
The lessons should form a DAG, where the edges represents the prerequisites for each lesson.
Each lesson should have a list of its prerequisites, which must be previously defined lessons.
Hence, the order in which you output the lessons must be topologically sorted.
If a lesson has no prerequisites, use an empty list.
Format your output as follows:

LessonTree:
    L1: []
    L2: []
    L3:
        - L1
    L4:
        - L2
        - L3

{few_shot}

Subject: {subject}
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