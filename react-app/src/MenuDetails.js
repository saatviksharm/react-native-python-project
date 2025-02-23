import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./MenuDetails.css";

const MenuDetails = () => {
  const { restaurant } = useParams();
  const navigate = useNavigate();
  const [menu, setMenu] = useState(null);

  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/get-menu/${restaurant}`);
        const data = await response.json();
        setMenu(data.menu);

        // ✅ Ask the user what they want to order
        const speech = new SpeechSynthesisUtterance(`What would you like to order from ${restaurant}?`);
        window.speechSynthesis.speak(speech);

      } catch (error) {
        console.error("Error fetching menu:", error);
      }
    };

    fetchMenu();
  }, [restaurant]);

  if (!menu) {
    return <div>Loading menu...</div>;
  }

  return (
    <div className="menu-details-container">
      <h1>{restaurant} Menu</h1>
      <ul>
        {Object.keys(menu).map((category, index) => (
          <li key={index}>
            <h2>{category}</h2>
            <ul>
              {menu[category].map((item, i) => (
                <li key={i}>{item.name} - ${item.price.toFixed(2)}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      <button className="back-button" onClick={() => navigate("/")}>
        🔙 Back to Search
      </button>
    </div>
  );
};

export default MenuDetails;
