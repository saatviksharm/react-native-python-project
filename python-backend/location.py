print("Script is running...")

import geocoder

# Get current coordinates based on IP address
g = geocoder.ip('me')

# Debugging output
print(f"Geocoder response: {g}")

if g.latlng:
    # Print the latitude and longitude
    print(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")
else:
    print("Could not fetch location. The result is empty.")
