#!/usr/bin/env bash

echo "Fetching weather data for Ogden, UT..."

curl -s "https://wttr.in/Ogden+Utah?format=j1" -o weather.json

echo "Starting Streamlit dashboard..."
streamlit run app.py