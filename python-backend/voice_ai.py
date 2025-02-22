import openai
import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import spacy


# Set up OpenAI API Key


# Function to capture voice and convert to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        #print(OPENAI_API_KEY)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=None)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        if 'stop listening' in text:
            print("Ending listening...")
            # Remove the ending keyword from the result
            text = text.replace('stop listening', '').strip()
            return text

        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Network error.")
        return ""


# Function to process text with OpenAI
'''def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": question}
        ],
        max_tokens=50
    )
    #answer = response['choices'][0]['message']['content']
    answer = response.choices[0].message.content.strip()
    print(f"AI: {answer}")
    return answer
'''

# Function to convert text to speech and play audio using pygame
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up
    pygame.mixer.quit()
    os.remove(filename)


# Main loop to continuously listen, process, and speak
#if __name__ == "__main__":
    '''while True:
        print("\nSay 'exit' to stop.")
        user_input = listen().lower()
        if 'exit' in user_input:
            print("Goodbye!")
            speak("Goodbye!")
            break
        elif user_input:
            response = ask_openai(user_input)
            print(response)
            #speak(response)'''
speak(listen())
