import os
import datetime
import logging
from json import load, dump
from dotenv import dotenv_values
from groq import Groq

# Load environment variables
env_vars = dotenv_values(".env")
print("Loaded environment variables:", env_vars)  # Debug: Check loaded variables

# Provide default values for missing variables
Username = env_vars.get("username", "Rutuja")
Assistantname = env_vars.get("Atlas", "Atlas")
GroqAPIKey = env_vars.get("add your api key")


# Initialize Groq client
client = Groq(api_key="add youe api key ")

# Rest of the code remains the same...


# Set up logging
logging.basicConfig(filename="chatbot.log", level=logging.ERROR)

# Define file paths
chat_log_path = os.path.join("Data", "ChatLog.json")

# Initialize messages list
messages = []

# System prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System},
]

# Load chat history
try:
    with open(chat_log_path, "r") as file:
        messages = load(file)
except FileNotFoundError:
    with open(chat_log_path, "w") as file:
        dump([], file, indent=4)

# Realtime information function
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return {
        "day": current_date_time.strftime("%A"),
        "date": current_date_time.strftime("%d %B %Y"),
        "time": current_date_time.strftime("%H:%M:%S"),
    }

# Answer modifier function
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

# ChatBot function
def ChatBot(Query):
    try:
        with open(chat_log_path, "r") as file:
            messages = load(file)

        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot
            + [{"role": "system", "content": str(RealtimeInformation())}]
            + messages,
            max_tokens=1024,
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

        with open(chat_log_path, "w") as file:
            dump(messages, file, indent=4)

        return AnswerModifier(Answer)
    except Exception as e:
        logging.error(f"Error in ChatBot: {e}")
        return "Sorry, an error occurred while processing your request. Please try again later."

# Main loop
if __name__ == "__main__":
    print(f"Welcome! You are chatting with {Assistantname}. Type 'exit' to end the chat.")
    while True:
        user_input = input("Enter your Question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print(ChatBot(user_input))
