import openai
import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import spacy
import requests
from flask import Flask, request, jsonify
import requests
import geocoder
app = Flask(__name__)
#from app import test_yelp_connection
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp("This is a sentence.")
print([(w.text, w.pos_) for w in doc])
FLASK_API_URL = "http://127.0.0.1:5000"
# Set up OpenAI API Key

def get_user_location():
    """Fetch user's latitude and longitude based on IP address"""
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]  # Returns (latitude, longitude)
    return None, None  # Return None if location not found

# Replace with your actual Yelp API Key
YELP_API_KEY = "LYUR5jHjCNxHTpr5DdycC_awjt3k2Zu_nr_tALiFGclgLiBAVj1eshU4oN5AyjE91CLtX8-ato1eDLXnc9KHJn-b_W6MI77qM-_5DfF-F9X0hhtzY69MuETOoCi5Z3Yx"
YELP_API_URL = "https://api.yelp.com/v3/businesses/search"


#if __name__ == "__main__":
    #app.run(debug=True)

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
    
def extract_nouns(text):
    doc = nlp(text)
    nouns = []

    # Extract nouns from the text
    for token in doc:
        # Check if the token is a noun
        if token.pos_ == 'NOUN':
            nouns.append(token.text)

    # Remove duplicates
    nouns = list(set(nouns))

    # Only print if there are nouns
    if nouns:
        print(f"Nouns Detected: {nouns}")
        return nouns

def fetch_restaurants(nouns):
    if not nouns:
        print("No nouns detected, defaulting to 'restaurants'.")
        nouns = ["restaurants"]

    search_term = " ".join(nouns)  # Combine nouns into a single search term
    print(f"Searching for: {search_term}")

    restaurants = test_yelp_connection(search_term)  # ✅ Call function directly

    # 🔹 Print only restaurant names
    for restaurant in restaurants:
        print(restaurant)

    return restaurants
@app.route("/test-yelp", methods=["GET"])
def test_yelp_connection():

    user_lat,user_lng = get_user_location()

    if user_lat is None or user_lng is None:
        return jsonify({"error": "Could not determine location"}), 400
    
    nouns = extract_nouns(listen())
    search_term = " ".join(nouns)  # Combine nouns into a single search term
    print(f"Searching for: {search_term}")
    
    term = request.args.get("term", search_term)  # Default search term
    limit = request.args.get("limit", 5)  # Default limit

    """Test if the backend can connect to Yelp API"""
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
            "term": term,
            "latitude": user_lat,
            "longitude": user_lng,
            "limit": limit,
        }

    response = requests.get(YELP_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        restaurants = [business["name"] for business in data.get("businesses", [])]  # Extract names
        return jsonify({
            "message": "Successfully connected to Yelp API!",
            "restaurant_names": restaurants  # Send only restaurant names
        })
    else:
        return jsonify({"error": "Failed to connect to Yelp API"}), response.status_code
    
# Main function to listen, extract nouns, and fetch restaurants
def main():
    user_input = listen()
    nouns = extract_nouns(user_input)
    test_yelp_connection(nouns)  # ✅ Uses direct function call

if __name__ == "__main__":
    app.run(debug=True)
    
speak(listen())

