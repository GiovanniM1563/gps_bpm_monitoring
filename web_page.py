import streamlit as st
import pandas as pd
import GPSUtil as gps
import osmnx as ox
import time
import folium

def webpage():
    """
    Display the contents of a variable and coordinates in real-time on a Streamlit webpage.
    """

    # Create a Streamlit app
    st.title("Real-time Variable and Coordinates Display")

    # Create a layout with two columns
    col1, col2 = st.columns([2, 1])

    # Display the variable on the left side
    with col1:
        st.header("Heart Rate (BPM)")
        text_placeholder = st.empty()  # Placeholder for the text

    # Display the coordinates and map on the right side
    with col2:
        st.header("Current Location")
        latitude_placeholder = st.empty()  # Placeholder for latitude
        longitude_placeholder = st.empty()  # Placeholder for longitude

    # Get GPS coordinates
    cur_lat, cur_long = gps.get_gps_readout()

    if cur_lat is None or cur_long is None:
        st.error("No GPS data available!")
        return
    else:
        # Convert latitude and longitude to float
        cur_lat = float(cur_lat)
        cur_long = float(cur_long)

        # Update latitude and longitude placeholders
        latitude_placeholder.write("Latitude: {}".format(cur_lat))
        longitude_placeholder.write("Longitude: {}".format(cur_long))

        display_df = pd.DataFrame({"latitude": [cur_lat], "longitude": [cur_long]})

        # Display map
        st.map(latitude=cur_lat, longitude=cur_lat, data= display_df, zoom=9)

    # Set up periodic updates every second
    st.rerun()

# Example usage:
webpage()
