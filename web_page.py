import streamlit as st
import pandas as pd
import GPSUtil as gps
import osmnx as ox
import time
import folium
import serial as bpm
#from bpm_read import bpm_reading

def webpage():
    """
    Display the contents of a variable and coordinates in real-time on a Streamlit webpage.

    Parameters:
        my_variable (str): The variable whose contents will be displayed.
        latitude (float): The latitude value.
        longitude (float): The longitude value.
    """

    #initialize time 
    st.session_state.start_time = time.time()

    # Create a 
    # DataFrame with the coordinates
    cur_lat, cur_long = gps.get_gps_readout() 

    display_df = pd.DataFrame({
        'LATITUDE': [cur_lat],
        'LONGITUDE': [cur_long]
    })
    
    location_history = pd.DataFrame({
        'LATITUDE': [],
        'LONGITUDE': [],
        "TIME": pd.Timestamp.now()
     })
    
    # Create a Folium map centered at the given coordinates
    current_location_map = folium.Map(location=[cur_lat, cur_long], zoom_start=15)

    # Add a marker at the given coordinates
    folium.Marker([cur_lat, cur_long]).add_to(current_location_map)

    asset = current_location_map

    # Get the BPM reading
    BPM = bpm.get_reading()

    # if three have passed
    if time.time() - st.session_state.start_time >= 10:
        location_history = location_history.append(display_df, ignore_index=True)
        st.session_state.start_time = time.time()

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
        st.write("Nearest Address:", gps.get_address(cur_lat, cur_long))



    # Display the map
    st.components.v1.html(asset.render(), width=800, height=600)
    # if st.button is clicked, generate route
    if st.button("Show Route"):
        nodes = gps.get_nearest_nodes(location_history)
        route, _, _ = gps.generate_route(nodes)
        asset = route

    if st.button("Show Current Location"):
        asset = current_location_map




    st.dataframe(location_history)





# Example usage:


webpage()
