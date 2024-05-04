import streamlit as st
import ast
import sqlite3
import datetime
import GPSUtil

def create_new_database(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS db(lat TEXT, long TEXT)')
    con.commit()
    return con

def add_new_row(con, lat, long):
    cur = con.cursor()
    cur.execute('INSERT INTO db VALUES (?, ?)', (lat, long))
    con.commit()

def test_gps_readout():
    # Call the function to get GPS readout
    gps_readout = GPSUtil.get_gps_readout()

    # Check if the function returned None
    if gps_readout is None:
        # Handle the case where GPS readout is not available
        print("GPS readout is not available")
    else:
        # Unpack the GPS readout into latitude and longitude
        cur_lat, cur_long = gps_readout
        print("Latitude:", cur_lat)
        print("Longitude:", cur_long)
        add_new_row(gps_table, cur_lat, cur_long)


gps_table = create_new_database('gps_data.db')

st.title("Real-time GPS Data Collection")

#display most recent GPS data from the database
cur = gps_table.cursor()
cur.execute('SELECT * FROM db ORDER BY ROWID DESC LIMIT 1')
latest_data = cur.fetchone()

if latest_data is not None:
    st.write("Most recent GPS data:")
    st.write("Latitude:", latest_data[0])
    st.write("Longitude:", latest_data[1])