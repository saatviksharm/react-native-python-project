from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Yelp API Key
YELP_API_KEY = "LYUR5jHjCNxHTpr5DdycC_awjt3k2Zu_nr_tALiFGclgLiBAVj1eshU4oN5AyjE91CLtX8-ato1eDLXnc9KHJn-b_W6MI77qM-_5DfF-F9X0hhtzY69MuETOoCi5Z3Yx"
YELP_API_URL = "https://api.yelp.com/v3/businesses/search"

@app.route("/test-yelp", methods=["GET"])
def test_yelp_connection():
    """Test if the backend can connect to Yelp API"""
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"term": "pizza", "location": "New York", "limit": 5}

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
