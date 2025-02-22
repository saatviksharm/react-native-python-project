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

FOOD_LIST = {
    # Fast Foods
    "burger", "cheeseburger", "bacon burger", "big mac", "whopper", "chicken sandwich",
    "fish sandwich", "grilled cheese", "pulled pork", "philly cheesesteak", "sloppy joe",
    "hot dog", "corn dog", "fried chicken", "chicken nuggets", "chicken tenders",
    "popcorn chicken", "onion rings", "french fries", "mozzarella sticks", "curly fries",
    "nachos", "tacos", "burritos", "quesadillas", "chimichangas", "enchiladas",
    
    # Pizza & Italian Foods
    "pizza", "pepperoni pizza", "cheese pizza", "bbq chicken pizza", "hawaiian pizza",
    "stromboli", "calzone", "garlic knots", "lasagna", "spaghetti", "fettuccine alfredo",
    "ravioli", "carbonara", "gnocchi", "risotto",

    # Asian Foods
    "sushi", "nigiri", "maki", "sashimi", "poke bowl", "ramen", "pho", "udon",
    "teriyaki chicken", "sweet and sour chicken", "general tso’s chicken",
    "egg rolls", "dumplings", "spring rolls", "lo mein", "pad thai", "bibimbap",
    
    # Seafood & Expensive Foods
    "lobster", "crab", "king crab", "snow crab", "shrimp", "prawns", "oysters", "scallops",
    "mussels", "clams", "caviar", "uni", "foie gras", "wagyu beef", "truffles",
    
    # Vegetables
    "broccoli", "carrots", "spinach", "potatoes", "sweet potatoes", "onions", "garlic",
    "lettuce", "cucumber", "mushrooms", "avocado", "eggplant", "cabbage", "cauliflower",
    "asparagus", "zucchini", "brussels sprouts", "peppers", "jalapenos", "artichokes",
    
    # Fruits
    "apple", "banana", "strawberry", "blueberry", "raspberry", "blackberry",
    "orange", "lemon", "lime", "pineapple", "mango", "grapefruit", "kiwi", "pomegranate",
    "grapes", "pear", "watermelon", "cantaloupe", "honeydew", "dragon fruit", "passion fruit",

    # Desserts
    "chocolate cake", "vanilla cake", "cheesecake", "brownies", "cookies", "ice cream",
    "milkshake", "doughnuts", "churros", "apple pie", "sundae", "tiramisu", "pudding",
    "mousse", "cupcakes", "macarons", "scones", "mille-feuille",
    
    # Beverages
    "coffee", "latte", "cappuccino", "espresso", "tea", "bubble tea", "matcha", "smoothie",
    "milkshake", "soda", "coke", "pepsi", "sprite", "lemonade", "mojito"
}


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
        speak("Sorry, I did not understand that")
        return ""
    except sr.RequestError:
        print("Network error.")
        speak("Sorry, I did not understand that")
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
    extracted_nouns = set()
    
    # ✅ Convert text to lowercase for case-insensitive matching
    words = text.lower().split()
    found_food = False

    # ✅ Check for food-related phrases in the sentence
    for phrase in FOOD_LIST:
        phrase_words = phrase.lower().split()
        if all(word in words for word in phrase_words):  # If phrase exists in the sentence
            extracted_nouns.add(phrase)
            found_food = True  # ✅ Mark that we found a food phrase

    # ✅ Process nouns detected by NLP
    for token in doc:
        if token.pos_ == "NOUN":
            noun = token.text.lower()
            if noun in FOOD_LIST or found_food:  # ✅ Keep if it's in the food list or a phrase was found
                extracted_nouns.add(noun)

    if extracted_nouns:
        print(f"Filtered Nouns Detected: {extracted_nouns}")
        return list(extracted_nouns)
    else:
        speak("Sorry I do not understand that. Please try again.")
        print("No valid food items detected.")
        return []


@app.route("/test-yelp", methods=["GET"])
def test_yelp_connection():

    user_lat,user_lng = get_user_location()

    if user_lat is None or user_lng is None:
        return jsonify({"error": "Could not determine location"}), 400
    
    speak("What would you like to search for?")
    
    nouns = extract_nouns(listen())

    if nouns == []:
        return

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

