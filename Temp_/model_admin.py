import streamlit as st
import pymongo
import pandas as pd
import time

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["smart_cooling"]
sensor_collection = db["sensor_data"]

# --- Login System ---
st.title("Admin Dashboard - Smart Cooling System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Display login section only if user is not logged in
if not st.session_state.logged_in:
    username = st.text_input("Username", "")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "ganesh" and password == "ganesh":
            st.session_state.logged_in = True
            st.success("Login successful!")
            time.sleep(1)  # Small delay to simulate login process
            st.rerun()  # Refresh the page after login
        else:
            st.error("Invalid credentials")
else:
    # After login, the dashboard will be shown
    # --- Sidebar: Mode Selection ---
    st.sidebar.header("Mode Selection")
    mode = st.sidebar.radio("Select Mode", ["Manual Mode", "AI Agent Mode"])
    sub_mode = st.sidebar.radio("Select Sub-Mode", ["Normal Mode", "Zone Mode"])

    # --- Real-time Sensor Data Display ---
    st.header("Real-time Sensor Data (Last 5 Records)")
    sensor_data = list(sensor_collection.find().sort("timestamp", -1).limit(5))

    # Flatten the data (Convert lists into individual rows)
    flat_data = []
    for record in sensor_data:
        timestamp = record["timestamp"]
        for i in range(len(record["temperature"])):
            flat_data.append({
                "timestamp": timestamp,
                "temperature": record["temperature"][i],
                "humidity": record["humidity"][i],
                "fan_speed": record["fan_speed"][i],
                "data_cube": i + 1  # To identify DataCube 1, 2, 3
            })

    # Convert to DataFrame
    df = pd.DataFrame(flat_data)

    # Display Data
    st.dataframe(df)

    # --- Manual Mode Control ---
    if mode == "Manual Mode":
        st.header("Manual Control")
        fan_speeds = []
        humidity_values = []

        for i in range(1, 4):
            col1, col2 = st.columns(2)
            with col1:
                fan_speeds.append(st.number_input(f"Fan Speed for Data Cube {i}", min_value=0, max_value=100, step=1))
            with col2:
                humidity_values.append(st.number_input(f"Humidity for Data Cube {i}", min_value=0, max_value=100, step=1))

        if st.button("Update Manual Settings"):
            update_data = {"fan_speeds": fan_speeds, "humidity_values": humidity_values, "timestamp": time.time()}
            manual_control_collection.insert_one(update_data)
            st.success("Manual settings updated!")

    # --- AI Agent Mode Display ---
    if mode == "AI Agent Mode":
        st.header("AI Agent Mode Display")
        
        sensor_data = list(sensor_collection.find().sort("timestamp", -1).limit(3))
        if sensor_data:
            st.write("Latest AI Adjusted Values:")
            for idx, data in enumerate(sensor_data):
                st.write(f"Data Cube {idx + 1}: Fan Speed = {data['fan_speed']}, Humidity = {data['humidity']}")
        else:
            st.warning("No AI data available yet.")

    # --- Link to Dash Dashboard ---
    st.sidebar.header("View Real-Time Analytics Dashboard")
    st.sidebar.markdown("[Click here to view the Dash Dashboard](http://localhost:8050)")
