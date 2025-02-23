import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Results.css";

const Results = () => {
  const navigate = useNavigate();
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [order, setOrder] = useState("");
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const storedData = localStorage.getItem("restaurants");
    if (storedData) {
      setRestaurants(JSON.parse(storedData));
    } else {
      navigate("/"); // Redirect if no restaurant data
    }
  }, [navigate]);

  // ✅ Function to show the popup and ask for an order
  const startOrderProcess = (restaurant) => {
    setSelectedRestaurant(restaurant);
    setShowPopup(true);
  };

  // ✅ Function to place an order and navigate to Google Maps
  const placeOrder = () => {
    if (!selectedRestaurant) return;

    // ✅ Speak "Order placed!"
    const speech = new SpeechSynthesisUtterance("Order placed!");
    window.speechSynthesis.speak(speech);

    // ✅ Open Google Maps with restaurant location
    const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(selectedRestaurant.address)}`;
    window.open(googleMapsUrl, "_blank");

    // ✅ Close the popup
    setShowPopup(false);
  };

  return (
    <div className="results-container">
      <h1>Restaurants Found</h1>
      <div className="restaurant-list">
        {restaurants.map((restaurant, index) => (
          <div
            key={index}
            className="restaurant-card"
            onClick={() => startOrderProcess(restaurant)} // ✅ Show order popup when clicked
          >
            <img src={restaurant.image_url} alt={restaurant.name} />
            <h2>{restaurant.name}</h2>
            <p>{restaurant.address}</p>
            <p>⭐ {restaurant.rating} | {restaurant.price}</p>
          </div>
        ))}
      </div>

      {/* ✅ Order Popup */}
      {showPopup && selectedRestaurant && (
        <div className="popup">
          <h2>What would you like to order from {selectedRestaurant.name}?</h2>
          <input
            type="text"
            placeholder="Type your order here..."
            value={order}
            onChange={(e) => setOrder(e.target.value)}
          />
          <button onClick={placeOrder}>Place Order</button>
          <button className="cancel" onClick={() => setShowPopup(false)}>Cancel</button>
        </div>
      )}

      <button className="back-button" onClick={() => navigate("/")}>
        🔙 Back to Search
      </button>
    </div>
  );
};

export default Results;
