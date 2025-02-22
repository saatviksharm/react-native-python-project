import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  FlatList,
  StyleSheet,
} from "react-native";
import LinearGradient from "react-native-linear-gradient";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";

const HomeScreen = () => {
  const [listening, setListening] = useState(false);
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null); // Function to handle voice input and fetch restaurants

  const handleVoiceInput = async () => {
    setListening(true);
    setLoading(true);
    setError(null);
    setRestaurants([]);

    try {
      const response = await fetch("http://127.0.0.1:5000/listen", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        setRestaurants(data.restaurants);
      }
    } catch (err) {
      setError("Could not connect to server.");
    }

    setListening(false);
    setLoading(false);
  };

  return (
    <LinearGradient colors={["#0072ff", "#00c6ff"]} style={styles.container}>
      <Text style={styles.title}>Voice Search Restaurants</Text>

      <TouchableOpacity
        style={styles.micButton}
        onPress={handleVoiceInput}
        disabled={listening}
      >
        <Icon
          name={listening ? "microphone-off" : "microphone"}
          size={50}
          color="#fff"
        />
      </TouchableOpacity>
      {loading && <ActivityIndicator size="large" color="#fff" />}
      {error && <Text style={styles.error}>{error}</Text>}

      <FlatList
        data={restaurants}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.restaurantItem}>
            <Text style={styles.restaurantText}>{item}</Text>
          </View>
        )}
      />
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 20,
  },
  micButton: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 20,
  },
  error: {
    color: "red",
    fontSize: 16,
    marginTop: 10,
  },
  restaurantItem: {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    padding: 10,
    marginVertical: 5,
    borderRadius: 5,
  },
  restaurantText: {
    color: "#fff",
    fontSize: 18,
  },
});

export default HomeScreen;
