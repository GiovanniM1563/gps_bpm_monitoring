import osmnx as ox
import folium
import serial
import time     
import GPSUtil
nodes = []



while True:
    #get the current location of the GPS module
    lat, lng = GPSUtil.get_gps_readout()

    #Create a map with a marker at the current location
    marker = GPSUtil.create_map_marker(lat, lng, "Click For Details")

    marker.show_in_browser()

    #Get the node id of the current location    
    node = GPSUtil.get_node(lat, lng)

    #Add the node id to the list of nodes   
    nodes.append(node)

    #Section of code that checks for heartrate
    #if heartrate is above 150 or lower than 60, stop tracking aka break out of loop


print("Patient in distress, check map for location")
#Generate a route based on the list of nodes
GPSUtil.generate_route(nodes)

#needs to send all of the created data to monitored device