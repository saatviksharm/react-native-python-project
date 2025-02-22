#!/bin/bash
echo "Starting Flask..."
cd ../python-backend  # Adjust this path based on where yelp-and-speak.py is located
python yelp-and-speak.py &  # Run Flask in the background

echo "Starting React..."
cd ../react-app  # Adjust this path if needed
npm start
