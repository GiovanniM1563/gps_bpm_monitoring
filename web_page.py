import streamlit as st
import pandas as pd
#import GPSUtil as gps
import osmnx as ox
import time
import folium
#import transfer as bpm
#from bpm_read import bpm_reading

def webpage(cur_lat, cur_long, bpm):
    """
    Display the contents of a variable and coordinates in real-time on a Streamlit webpage.

    Parameters:
        my_variable (str): The variable whose contents will be displayed.
        latitude (float): The latitude value.
        longitude (float): The longitude value.
    """

    #initialize time 
    st.session_state.start_time = time.time()

    if bpm is None:
        BPM = "No data available"

    if cur_lat is None:
        cur_lat = "No data available"
        cur_long = "No data available"

    display_df = pd.DataFrame({
        'LATITUDE': [cur_lat],
        'LONGITUDE': [cur_long]
    })
    
    # Create a Streamlit app
    st.title("Real-time Variable and Coordinates Display")

    # Create a layout with two columns
    col1, col2 = st.columns([2, 1])

    # Display the variable on the left side
    with col1:
        st.header("Heart Rate (BPM)")
        text_placeholder = st.empty()  # Placeholder for the text
        text_placeholder.text(BPM)

    # Display the coordinates and map on the right side
    with col2:
        st.header("Current Location")
        st.write("Latitude:", cur_lat)
        st.write("Longitude:", cur_long)
        #st.write("Nearest Address:", gps.get_address(cur_lat, cur_long))





# Example usage:


webpage(None, None, None)
