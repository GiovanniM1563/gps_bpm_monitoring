import streamlit as st
import sqlite3
import pandas as pd
import datetime
import GPSUtil
import transfer
import time

def create_gps_database(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS gps_data(lat REAL, long REAL, time TIMESTAMP)')
    con.commit()
    return con

def create_bpm_database(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS bpm_data(bpm TEXT)')
    con.commit()
    return con

def add_new_row_gps(con, lat, long, time):
    cur = con.cursor()
    cur.execute('INSERT INTO gps_data VALUES (?, ?, ?)', (lat, long, time))
    con.commit()

def add_new_row_bpm(con, bpm):
    cur = con.cursor()
    cur.execute('INSERT INTO bpm_data VALUES (?)', (bpm,))
    con.commit()

def get_latest_gps_data(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM gps_data WHERE lat IS NOT NULL AND long IS NOT NULL ORDER BY time DESC LIMIT 1')
    return cur.fetchone()

def get_latest_bpm_data(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM bpm_data WHERE bpm IS NOT NULL ORDER BY ROWID DESC LIMIT 1')
    return cur.fetchone()

def test_gps_readout():
    gps_readout = GPSUtil.get_gps_readout()
    if gps_readout:
        cur_lat, cur_long = gps_readout
        time_now = datetime.datetime.now()
        add_new_row_gps(gps_table, cur_lat, cur_long, time_now)
        print("Latitude:", cur_lat)
        print("Longitude:", cur_long)
    else:
        print("GPS readout is not available")

def test_bpm_readout():
    bpm_readout = transfer.get_reading()
    if bpm_readout and bpm_readout != "1":
        add_new_row_bpm(bpm_table, bpm_readout)
        print("BPM:", bpm_readout)
    else:
        print("BPM readout is not available")

gps_table = create_gps_database('gps_data.db')
bpm_table = create_bpm_database('bpm_data.db')

test_gps_readout()
test_bpm_readout()

st.title("Real-time Data Collection")

# Create a layout with two columns
col1, col2 = st.columns(2)

# Display GPS data in the first column
with col1:
    st.title("GPS Data")
    latest_gps_data = get_latest_gps_data(gps_table)
    if latest_gps_data:
        st.write("Most recent GPS data:")
        st.write("Latitude:", latest_gps_data[0])
        lat = latest_gps_data[0]
        st.write("Longitude:", latest_gps_data[1])
        long = latest_gps_data[1]
        st.write("Time:", latest_gps_data[2])
    else:
        st.write("No GPS data available. Fetching most recent from the database.")
        latest_gps_data_db = get_latest_gps_data(gps_table)
        if latest_gps_data_db:
            st.write("Most recent GPS data from database:")
            st.write("Latitude:", latest_gps_data_db[0])
            lat = latest_gps_data_db[0]
            st.write("Longitude:", latest_gps_data_db[1])
            long = latest_gps_data_db[1]
            st.write("Time:", latest_gps_data_db[2])
        else:
            st.write("No GPS data available in the database.")

# Display BPM data in the second column
with col2:
    st.title("BPM Data")
    latest_bpm_data = get_latest_bpm_data(bpm_table)
    if latest_bpm_data:
        st.write("Most recent BPM data:")
        st.write("BPM:", latest_bpm_data[0])
    else:
        st.write("No BPM data available. Fetching most recent from the database.")
        latest_bpm_data_db = get_latest_bpm_data(bpm_table)
        if latest_bpm_data_db:
            st.write("Most recent BPM data from database:")
            st.write("BPM:", latest_bpm_data_db[0])
        else:
            st.write("No BPM data available in the database.")

# Create a DataFrame with the most recent latitude and longitude
if latest_gps_data:
    lat = float(lat)
    long = float(long)
    df = pd.DataFrame({'latitude': [lat], 'longitude': [long]})
    st.title("Map")
    st.map(df)


time.sleep(60)

st.experimental_rerun()
