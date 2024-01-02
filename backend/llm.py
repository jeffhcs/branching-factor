from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def prompt_llm(prompt):
    stream = client.chat.completions.create(
    # model="gpt-3.5-turbo-1106",
    model="gpt-3.5-turbo",
    # model="gpt-4",
    # model="gpt-4-1106-preview",
    messages=[{"role": "user", "content": prompt}],
    stream=True,
)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="")
                yield chunk.choices[0].delta.content

def prompt_llm_instruct(prompt):
    stream = client.completions.create(
    # model="gpt-3.5-turbo-1106",
    model="gpt-3.5-turbo-instruct",
    # model="gpt-4",
    # model="gpt-4-1106-preview",
    prompt=prompt,
    max_tokens=1000,
    stream=True,
)
    for chunk in stream:
        if chunk.choices[0].text is not None:
            # print(chunk.choices[0].delta.content, end="")
            yield chunk.choices[0].text
    # return stream


if __name__ == "__main__":
    prompt = "List the first 50 elements of the periodic table."
    # prompt_llm(prompt)
    for chunk in prompt_llm(prompt):
        print(chunk, end="")
