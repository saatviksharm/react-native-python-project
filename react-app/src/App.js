import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

const App = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  // Function to fetch restaurant data from Flask backend
  const fetchRestaurants = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/test-yelp");
      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        localStorage.setItem("restaurants", JSON.stringify(data.restaurants)); // Store data
        navigate("/results"); // Redirect to results page
      }
    } catch (err) {
      setError("Could not connect to Flask server.");
    }
  };

  return (
    <div className="App">
      <h1>Listening for Restaurants...</h1>

      <button className="mic-button" onClick={fetchRestaurants}>
        🎤 Search Restaurants
      </button>

      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default App;
