import streamlit as st
import pandas as pd
import json
import os

st.title("Live Weather Dashboard")

# 1. Load the data
file_name = "weather.json"

if os.path.exists(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)

    # 2. Extract Key Info
    # The JSON structure from wttr.in is nested, so we dig in:
    current = data['current_condition'][0]
    location = data['nearest_area'][0]['areaName'][0]['value']
    
    # 3. Display Current Conditions
    st.header(f"Weather in {location}")
    
    # Create three columns for neat metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{current['temp_F']}°F")
    col2.metric("Humidity", f"{current['humidity']}%")
    col3.metric("Wind", f"{current['windspeedKmph']} km/h")

    # 4. Visualization: 3-Day Forecast
    st.subheader("3-Day Temperature Forecast")
    
    # Extract forecast data for the chart
    forecast_data = []
    for day in data['weather']:
        forecast_data.append({
            "Date": day['date'],
            "Max Temp (F)": int(day['maxtempF']),
            "Min Temp (F)": int(day['mintempF'])
        })
    
    # Convert to DataFrame and display chart
    df = pd.DataFrame(forecast_data)
    st.bar_chart(df.set_index("Date"))

else:
    st.error("Data file not found. Please run ./run_dashboard.sh to fetch data.")