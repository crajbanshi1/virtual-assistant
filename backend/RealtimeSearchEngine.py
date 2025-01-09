from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

SystemChatBot = [{"role": "system", "content": System}]


try:
    with open(r"data\Chatlog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"data\Chatlog.json", "w") as f:
        dump([], f)


def GoogleSearch(query):
    result = list(search(query, advanced=True, num_results=5))
    Answer = f"The search result for '{query}' are\n[start]\n"

    for i in result:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n"

    Answer += "[end]"
    return Answer


def AnswerModifier(Answer: str):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modidied_answer = "\n".join(non_empty_lines)
    return modidied_answer


SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"},
]


def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} secondn"
    return data


def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    try:

        with open(r"data\Chatlog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{prompt}"})

        SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot
            + [{"role": "system", "content": Information()}]
            + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"data\Chatlog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    except Exception as e:

        print(f"Error: {e}")
        with open(r"data\Chatlog.json", "w") as f:
            dump([], f, indent=4)
        return RealtimeSearchEngine(prompt)


if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Query: ")
        print(RealtimeSearchEngine(user_input))
