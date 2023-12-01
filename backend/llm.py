from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def prompt_llm(prompt):
    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # model="gpt-4-1106-preview",
    messages=[{"role": "user", "content": prompt}],
    stream=True,
)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="")
            yield chunk.choices[0].delta.content


if __name__ == "__main__":
    prompt = "List the first 20 elements"
    # prompt_llm(prompt)
    for chunk in prompt_llm(prompt):
        print(chunk, end="")
