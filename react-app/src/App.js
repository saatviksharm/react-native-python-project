import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";
import { FaMicrophone } from 'react-icons/fa';

const App = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const abortControllerRef = useRef(null);
  const isFetchingRef = useRef(false);

  const toggleListening = () => {
    if (isListening) {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort(); // Cancel the fetch request
        abortControllerRef.current = null;
        isFetchingRef.current = false;
      }
      setIsListening(false);
    } else {
      // Start a new fetch request
      setIsListening(true);
      fetchRestaurants();
    }
  };

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
      //setError("Could not connect to Flask server.");
    } finally {
      setIsListening(false); // Reset listening state after fetch completes or is aborted
    }
  };

  return (
    <div className="App gradient-background">
      <h1 className="title-text">Find Restaurants Near You</h1>
      <FaMicrophone className="mic-button" onClick={toggleListening}/>
      {isListening && <div className="wave wave1"></div>}
        {isListening && <div className="wave wave2"></div>}
        {isListening && <div className="wave wave3"></div>}

      {error && <p className="error">{error}</p>}
      <p className="bottom-text">{isListening ? "Listening..." : "Click to Speak"}</p>
    </div>
  );
};

export default App;
