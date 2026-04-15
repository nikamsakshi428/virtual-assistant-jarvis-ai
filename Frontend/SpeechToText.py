from dotenv import dotenv_values
import os
import mtranslate as mt
import speech_recognition as sr

env_vars = dotenv_values(".env")

InputLanguage = env_vars.get("InputLanguage")

TempDirPath = rf"{os.getcwd()}/Frontend/Files"

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)
        
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "which", "why", "can you", "whom", "whose", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening...")
        SetAssistantStatus("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        Text = recognizer.recognize_google(audio, language=InputLanguage)
        print(f"Recognized: {Text}")

        if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
            return QueryModifier(Text)
        else:
            SetAssistantStatus("Translating...")
            return QueryModifier(UniversalTranslator(Text))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return None

if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        if Text:
            print(Text)