from openai import OpenAI
from dotenv import load_dotenv
import os
import fcntl
import time

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def prompt_llm(prompt):

    while(not acquire_lock()):
        print("Waiting for lock...")
        time.sleep(1)

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

# def prompt_llm_instruct(prompt):
#     stream = client.completions.create(
#     # model="gpt-3.5-turbo-1106",
#     model="gpt-3.5-turbo-instruct",
#     # model="gpt-4",
#     # model="gpt-4-1106-preview",
#     prompt=prompt,
#     max_tokens=1000,
#     stream=True,
# )
#     for chunk in stream:
#         if chunk.choices[0].text is not None:
#             # print(chunk.choices[0].delta.content, end="")
#             yield chunk.choices[0].text
#     # return stream
def acquire_lock():
    lockfile = "/tmp/llm_global_lock"
    countfile = "/tmp/llm_global_lock_count"
    t_seconds = 1
    current_time = time.time()
    max_attempts = 100

    with open(lockfile, 'a+') as lock_file:
        try:
            # Try to acquire an exclusive lock
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Update and check lock count
            with open(countfile, 'a+') as count_file:
                count_file.seek(0)
                count_str = count_file.read().strip()
                count = int(count_str) if count_str else 0

                if count >= max_attempts:
                    return False  # Lock acquisition limit exceeded

                # Increment lock acquisition count
                count_file.seek(0)
                count_file.truncate()
                count_file.write(str(count + 1))
                count_file.flush()

            # Go to the start of the lock file and read the time
            lock_file.seek(0)
            time_str = lock_file.read().strip()
            lock_time = float(time_str) if time_str else 0

            if current_time >= lock_time:
                # Current time is past the lock time, can acquire lock
                # Write new lock time
                lock_file.seek(0)
                lock_file.truncate()
                lock_file.write(str(current_time + t_seconds))
                lock_file.flush()
                return True  # Lock acquired
            else:
                return False  # Lock is still held
        except BlockingIOError:
            return False  # Unable to acquire lock
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)

if __name__ == "__main__":
    prompt = "List the first 5 elements of the periodic table."
    # prompt_llm(prompt)
    for chunk in prompt_llm(prompt):
        print(chunk, end="")
