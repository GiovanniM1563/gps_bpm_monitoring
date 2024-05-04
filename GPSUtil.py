import serial 
import time 
import folium
import osmnx as ox
import geopy
from geopy.geocoders import Nominatim
import serial
import time

def get_gps_readout(timeout=1):
    start_time = time.time()  # Record the start time
    try:
        # Open serial connection
        with serial.Serial("COM6", baudrate=9600) as gps:
            # Set timeout for readline method
            gps.timeout = timeout
            # Read data from serial port
            line = gps.readline().decode().strip()
            while time.time() - start_time < timeout:
                if line.startswith("$GPRMC"):
                    data = line.split(",")
                    if data[2] == "A":
                        curr_lat_nmea = data[3]
                        curr_lat_deg = curr_lat_nmea[:2]
                        if data[4] == 'S':
                            lat = float(curr_lat_deg) * -1
                        else:
                            lat = float(curr_lat_deg)
                        lat_ddd = curr_lat_nmea[2:10]
                        lat_mmm = float(lat_ddd) / 60
                        lat_final = round(lat + lat_mmm, 6)

                        curr_long_nmea = data[5]
                        curr_long_deg = curr_long_nmea[0:3]
                        if data[6] == 'W':
                            long = float(curr_long_deg) * -1
                        else:
                            long = float(curr_long_deg)
                        long_ddd = curr_long_nmea[3:10]
                        long_mmm = float(long_ddd) / 60
                        long_final = round(long + long_mmm, 6)

                        print("Latitude:", lat_final)
                        print("Longitude:", long_final)
                        return lat_final, long_final
                    else:
                        line = gps.readline().decode().strip()  # Read next line
    except serial.SerialException as e:
        print("Serial communication error:", e)
    except Exception as e:
        print("Error:", e)
    
    # Return None if no GPS data is available or timeout occurs
    print("No GPS data received within {} seconds".format(timeout))
            
def create_map_marker(lat, lng, tooltip):
    m = folium.Map(location=[lat, lng], zoom_start=9, tiles="Stamen Terrain")

    folium.Marker(
    [lat, lng], popup="<i>Current Location</i>", tooltip=tooltip).add_to(m)
    m.save("tracker_test.html")
    time.sleep(5)
    return m

def get_node(latitude, longitude):
    place = 'Fullerton, California, United States'
    graph = ox.graph_from_place(place, network_type='walk', simplify=True, retain_all=False)
    node = ox.nearest_nodes(graph, longitude, latitude)
    return node

def get_nearest_nodes(location_history):
    nearest_nodes = []
    for index, row in location_history.iterrows():
        node = get_node(row['LATITUDE'], row['LONGITUDE'])
        nearest_nodes.append(node)
    return nearest_nodes

def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="gps_bpm_monitoring")
    location = geolocator.reverse((latitude, longitude))
    address = location.address
    return address

def generate_route(nodes):
    # create a graph from OSM within the boundaries of some geocodable place(s)
    place = 'Fullerton, California, United States'
    mode = 'walk'  # 'drive', 'bike', 'walk'
    graph = ox.graph_from_place(place, network_type=mode, simplify=True, retain_all=False)

    # find the nearest nodes in the graph for each node in the route
    nearest_nodes = [ox.nearest_nodes(graph, node[0], node[1]) for node in nodes]

    # find the shortest route based on the nodes
    shortest_route = ox.distance.shortest_path(graph, nearest_nodes, weight='length')

    # create a map viewable in HTML of the route
    route_map = ox.plot_route_folium(graph, shortest_route)

    # convert node ids to latitude and longitude
    list_of_x = [graph.nodes[node]['x'] for node in shortest_route]
    list_of_y = [graph.nodes[node]['y'] for node in shortest_route]

    return shortest_route, list_of_x, list_of_y    