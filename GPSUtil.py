import serial 
import time 
import folium
import osmnx as ox

def get_gps_readout():
    gps = serial.Serial("COM4", baudrate = 9600)
    line = gps.readline()
    data = line.decode().split(",")
    if data[0] == "$GPRMC":
        if data[2] == "A":
            curr_lat_nmea = data[3]
            curr_lat_deg = curr_lat_nmea[:2]
            if data[4] =='S':
                lat = float(curr_lat_deg) * -1
            else:
                lat = float(curr_lat_deg)
                lat = str(lat).strip('.')
                lat_ddd = curr_lat_nmea[2:10]
                lat_mmm = float(lat_ddd) / 60
                lat_mmm = str(lat_mmm).strip('0.')[:8]
                lat_final = lat + lat_mmm



                curr_long_nmea = data[5]
                curr_long_deg = curr_long_nmea[0:3]
                if data[6] == 'W':
                    long = float(curr_long_deg) * -1
                else:
                    long = float(curr_long_deg)
                long = str(long).strip('.0')
                long_ddd = curr_long_nmea[3:10]
                long_mmm = float(long_ddd) / 60
                long_mmm = str(long_mmm).strip('0.')[:9]
                long_final = long + "." + long_mmm

                print( lat_final, long_final)
                return lat_final,long_final
            
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
    route_map.save('route.html')

    # convert node ids to latitude and longitude
    list_of_x = [graph.nodes[node]['x'] for node in shortest_route]
    list_of_y = [graph.nodes[node]['y'] for node in shortest_route]

    return shortest_route, list_of_x, list_of_y    