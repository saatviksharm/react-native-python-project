import React, { useState, useEffect } from "react";
import "./App.css";

const App = () => {
  const [listening, setListening] = useState(true);
  const [restaurants, setRestaurants] = useState([]);
  const [error, setError] = useState(null);

  // Function to fetch restaurant data from Flask backend
  const fetchRestaurants = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/test-yelp");
      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        setRestaurants(data.restaurant_names);
        speakRestaurants(data.restaurant_names); // Speak results
      }
    } catch (err) {
      setError("Could not connect to Flask server.");
    }

    setListening(false);
  };

  // Function to speak restaurant names
  const speakRestaurants = (names) => {
    if (names.length > 0) {
      const message = `I found ${names.length} restaurants. ${names.join(", ")}`;
      const speech = new SpeechSynthesisUtterance(message);
      window.speechSynthesis.speak(speech);
    } else {
      const speech = new SpeechSynthesisUtterance("No restaurants found.");
      window.speechSynthesis.speak(speech);
    }
  };

  return (
    <div className="App">
      <h1>Listening for Restaurants...</h1>

      <button className="mic-button" onClick={fetchRestaurants}>
        🎤 Search Restaurants
      </button>

      {error && <p className="error">{error}</p>}
      {restaurants.length > 0 && (
        <div className="results">
          <h2>Restaurants Found:</h2>
          <ul>
            {restaurants.map((restaurant, index) => (
              <li key={index}>{restaurant}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;
