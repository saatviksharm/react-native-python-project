import openai
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound

# Set up OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to capture voice and convert to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Network error.")
        return ""

# Function to process text with OpenAI
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ],
        max_tokens=100
    )
    answer = response['choices'][0]['message']['content']
    print(f"AI: {answer}")
    return answer

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

# Main loop to continuously listen, process, and speak
def main():
    while True:
        print("\nSay 'exit' to stop.")
        user_input = listen().lower()
        if 'exit' in user_input:
            print("Goodbye!")
            speak("Goodbye!")
            break
        elif user_input:
            response = ask_openai(user_input)
            speak(response)

if __name__ == "__main__":
    main()
