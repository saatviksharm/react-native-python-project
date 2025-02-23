import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Results.css";

const Results = () => {
  const navigate = useNavigate();
  const [restaurants, setRestaurants] = useState([]);

  // ✅ Use useEffect to load restaurants only once when component mounts
  useEffect(() => {
    const storedData = localStorage.getItem("restaurants");
    if (storedData) {
      setRestaurants(JSON.parse(storedData));
    } else {
      navigate("/"); // Redirect to home if no data is found
    }
  }, [navigate]);

  // ✅ Navigate to the MenuDetails page for selected restaurant
  const openGoogleMaps = (address) => {
    const query = encodeURIComponent(address);
    const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${query}`;
    window.open(googleMapsUrl, "_blank");
  };

  return (
    <div className="results-container">
      <h1>Restaurants Found</h1>
      <div className="restaurant-list">
        {restaurants.map((restaurant, index) => (
          <div
            key={index}
            className="restaurant-card"
            onClick={() => openGoogleMaps(restaurant.address)} // ✅ Click to open MenuDetails
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
