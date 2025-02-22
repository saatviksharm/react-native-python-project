import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./MenuDetails.css";

const MenuDetails = () => {
  const { businessId } = useParams();
  const [menuDetails, setMenuDetails] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMenuDetails = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/get-menu/${businessId}`
        );
        const data = await response.json();
        setMenuDetails(data);
      } catch (error) {
        console.error("Error fetching menu details:", error);
      }
    };

    fetchMenuDetails();
  }, [businessId]);

  if (!menuDetails) {
    return <div>Loading menu details...</div>;
  }

  return (
    <div className="menu-details-container">
      <h1>{menuDetails.name}</h1>
      <img
        src={menuDetails.image_url}
        alt={menuDetails.name}
        className="menu-image"
      />
      <p>{menuDetails.location.display_address.join(", ")}</p>
      <p>⭐ {menuDetails.rating} | {menuDetails.price}</p>

      <h2>Menu</h2>
      <ul>
        {menuDetails.categories.map((category, index) => (
          <li key={index}>{category.title}</li>
        ))}
      </ul>

      <button className="back-button" onClick={() => navigate("/")}>
        🔙 Back to Search
      </button>
    </div>
  );
};

export default MenuDetails;
