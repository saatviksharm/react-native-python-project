import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Results.css";

const Results = () => {
  const navigate = useNavigate();
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    const storedData = localStorage.getItem("restaurants");
    if (storedData) {
      setRestaurants(JSON.parse(storedData));
    } else {
      navigate("/"); // Redirect to home if no data
    }
  }, [navigate]);

  // ✅ Function to open Google Maps with restaurant address
  const openGoogleMaps = (address) => {
    const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(
      address
    )}`;
    window.open(googleMapsUrl, "_blank"); // Opens in a new tab
  };

  return (
    <div className="results-container">
      <h1>Restaurants Found</h1>
      <div className="restaurant-list">
        {restaurants.map((restaurant, index) => (
          <div
            key={index}
            className="restaurant-card"
            onClick={() => openGoogleMaps(restaurant.address)} // ✅ Click opens Google Maps
          >
            <img src={restaurant.image_url} alt={restaurant.name} />
            <h2>{restaurant.name}</h2>
            <p>{restaurant.address}</p>
            <p>⭐ {restaurant.rating} | {restaurant.price}</p>
          </div>
        ))}
      </div>
      <button className="back-button" onClick={() => navigate("/")}>
        🔙 Back to Search
      </button>
    </div>
  );
};

export default Results;
