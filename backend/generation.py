from prompts import *
import yaml, json, re
from bson import ObjectId
from db import db

def create_notebook(prompt):
    output = ""
    for chunk in generate_syllabus(prompt):
        output += chunk
        yield chunk
    
    notebook = yaml.safe_load(output)
    notebook["intro"] = ""
    notebook["tree"] = ""

    notebook["syllabusText"] = yaml.dump(notebook["syllabus"])

    for unit in notebook["syllabus"]:
        unit_name, chapters = unit.popitem()
        unit["unit"] = unit_name
        unit["chapters"] = chapters
        for chapter in unit["chapters"]:
            chapter_name, lessons = chapter.popitem()
            chapter["chapter"] = chapter_name
            chapter["intro"] = ""
            chapter["lessons"] = [{"lesson": lesson_name, "content": ""} 
                                  for lesson_name in lessons]
                
    # print(json.dumps(notebook, indent=2))
    notebook_id = str(db.notebooks.insert_one(notebook).inserted_id)
    yield f"\nnotebook_id: {notebook_id}"

def get_tree(notebook_id):
    def get_chapters_from_syllabus(syllabus_text):
        def remove_prefixes(obj):
            if isinstance(obj, list):
                return [remove_prefixes(item) for item in obj]
            elif isinstance(obj, str):
                return re.sub(r'(Unit \d+: |Chapter \d+: |Lesson \d+\.\d+: )', '', obj)
            elif isinstance(obj, dict):
                return {remove_prefixes(key): remove_prefixes(value) for key, value in obj.items()}
            return obj

        def flatten_chapters(data):
            flattened = {}

            for unit_index, unit in enumerate(data):
                for chapters in unit.values():
                    for chapter_index, chapter in enumerate(chapters):
                        for chapter_name, lessons in chapter.items():
                            flattened[chapter_name] = {
                                "unit_index": unit_index,
                                "chapter_index": chapter_index,
                                "lessons": lessons
                            }

            return flattened

        class IndentDumper(yaml.Dumper):
            def increase_indent(self, flow=False, indentless=False):
                return super(IndentDumper, self).increase_indent(flow, False)
    
        obj = yaml.safe_load(syllabus_text)
        chapters_dict = flatten_chapters(remove_prefixes(obj))
        chapters_text = yaml.dump(chapters_dict, Dumper=IndentDumper, indent=4)
        chapters_text_indented = "\n".join([" "*4 + line for line in chapters_text.splitlines()])

        return chapters_dict, chapters_text_indented

    def parse_to_tree_elements(llm_output, chapters_dict):
        root_key = "ChaptersTree"
        try:
            cleaned_text = llm_output

            tree = yaml.safe_load(cleaned_text)

            elements = []

            for chapter, prerequisites in tree[root_key].items():
                elements.append({
                    "group": "nodes",
                    "data": {"id": chapter, 
                             "lessons": chapters_dict[chapter]["lessons"],
                             "unit_index": chapters_dict[chapter]["unit_index"],
                             "chapter_index": chapters_dict[chapter]["chapter_index"]}
                })

                for prereq in prerequisites:
                    elements.append({
                        "group": "edges",
                        "data": {"source": prereq, "target": chapter}
                    })

            return elements
        except Exception as e:
            print(e)
            return False

    # TODO: fix race condition with db

    notebook = db.notebooks.find_one({"_id": ObjectId(notebook_id)})
    if notebook["tree"] == "":
        chapters_dict, chapters_text = get_chapters_from_syllabus(notebook["syllabusText"])

        for attempts in range(3):
            tree_text = ""
            for chunk in generate_tree(chapters_text):
                tree_text += chunk
                # print(chunk, end="")
            tree = parse_to_tree_elements(tree_text, chapters_dict)

            if tree:
                break
            else:
                print("Failed tree. Trying again...")

        notebook["tree"] = tree
        db.notebooks.update_one({"_id": ObjectId(notebook_id)}, {"$set": {"tree": notebook["tree"]}})

        return tree
    else:
        return notebook["tree"]

def get_notebook_cover(notebook_id):
    notebook = db.notebooks.find_one({"_id": ObjectId(notebook_id)})
    if not notebook:
        return None
    cover = {
        "title": notebook["course"],
        "description": notebook["description"],
    }
    return cover

def get_chapter_intro(notebook_id, unit_index, chapter_index):

    notebook = db.notebooks.find_one({"_id": ObjectId(notebook_id)})
    if not notebook["syllabus"][unit_index]["chapters"][chapter_index]["intro"]:
        syllabus_text = notebook["syllabusText"]
        chapter_name = notebook["syllabus"][unit_index]["chapters"][chapter_index]["chapter"]

        chapter_content = ""
        for chunk in generate_chapter_intro(chapter_name, syllabus_text):
            chapter_content += chunk
            yield chunk
        
        notebook["syllabus"][unit_index]["chapters"][chapter_index]["intro"] = chapter_content
        db.notebooks.update_one({"_id": ObjectId(notebook_id)}, {"$set": {"syllabus": notebook["syllabus"]}})
    else:
        yield notebook["syllabus"][unit_index]["chapters"][chapter_index]["intro"]

def get_lesson_content(notebook_id, unit_index, chapter_index, lesson_index):

    notebook = db.notebooks.find_one({"_id": ObjectId(notebook_id)})
    if not notebook["syllabus"][unit_index]["chapters"][chapter_index]["lessons"][lesson_index]["content"]:
        syllabus_text = notebook["syllabusText"]
        lesson_name = notebook["syllabus"][unit_index]["chapters"][chapter_index]["lessons"][lesson_index]["lesson"]

        lesson_content = ""
        for chunk in generate_lesson(lesson_name, syllabus_text):
            lesson_content += chunk
            yield chunk
        
        notebook["syllabus"][unit_index]["chapters"][chapter_index]["lessons"][lesson_index]["content"] = lesson_content
        db.notebooks.update_one({"_id": ObjectId(notebook_id)}, {"$set": {"syllabus": notebook["syllabus"]}})
    else:
        yield notebook["syllabus"][unit_index]["chapters"][chapter_index]["lessons"][lesson_index]["content"]


if __name__ == "__main__":
    for chunk in getNotebook("machine learning"):
        # print(chunk, end="")
        pass