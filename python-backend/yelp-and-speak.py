import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import spacy
import requests
from flask import Flask, request, jsonify
import requests
import geocoder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Allow all origins (React frontend)

#from app import test_yelp_connection
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp("This is a sentence.")
print([(w.text, w.pos_) for w in doc])
FLASK_API_URL = "http://127.0.0.1:5000"

def get_user_location():
    """Fetch user's latitude and longitude based on IP address"""
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]  # Returns (latitude, longitude)
    return None, None  # Return None if location not found

# Replace with your actual Yelp API Key
YELP_API_KEY = "LYUR5jHjCNxHTpr5DdycC_awjt3k2Zu_nr_tALiFGclgLiBAVj1eshU4oN5AyjE91CLtX8-ato1eDLXnc9KHJn-b_W6MI77qM-_5DfF-F9X0hhtzY69MuETOoCi5Z3Yx"
YELP_API_URL = "https://api.yelp.com/v3/businesses/search"


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

@app.route("/test-yelp", methods=["GET"])
def test_yelp_connection():

    user_lat,user_lng = get_user_location()

    if user_lat is None or user_lng is None:
        return jsonify({"error": "Could not determine location"}), 400
    
    speak("What would you like to search for?")
    
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
    #data = response.json()
    #restaurants = [business["name"] for business in data.get("businesses", [])]  # Extract names
    #speak(restaurants)

    if response.status_code == 200:
        data = response.json()
        restaurants = []
        
        for business in data.get("businesses", []):
            restaurant_info = {
                "name": business["name"],
                "image_url": business["image_url"],
                "rating": business.get("rating", "N/A"),
                "address": ", ".join(business["location"]["display_address"]),
                "price": business.get("price", "N/A"),
                "url": business["url"],
            }
            restaurants.append(restaurant_info)
            speak(restaurant_info["name"])  # Speak out the restaurant names

        return jsonify({
            "message": "Successfully connected to Yelp API!",
            "restaurants": restaurants
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

