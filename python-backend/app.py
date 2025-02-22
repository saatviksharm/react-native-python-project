from flask import Flask, request, jsonify
import requests
import geocoder

app = Flask(__name__)

def get_user_location():
    """Fetch user's latitude and longitude based on IP address"""
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]  # Returns (latitude, longitude)
    return None, None  # Return None if location not found

# Replace with your actual Yelp API Key
YELP_API_KEY = "LYUR5jHjCNxHTpr5DdycC_awjt3k2Zu_nr_tALiFGclgLiBAVj1eshU4oN5AyjE91CLtX8-ato1eDLXnc9KHJn-b_W6MI77qM-_5DfF-F9X0hhtzY69MuETOoCi5Z3Yx"
YELP_API_URL = "https://api.yelp.com/v3/businesses/search"

@app.route("/test-yelp", methods=["GET"])
def test_yelp_connection():

    user_lat,user_lng = get_user_location()

    if user_lat is None or user_lng is None:
        return jsonify({"error": "Could not determine location"}), 400
    
    term = request.args.get("term", "restaurants")  # Default search term
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

if __name__ == "__main__":
    app.run(debug=True)
