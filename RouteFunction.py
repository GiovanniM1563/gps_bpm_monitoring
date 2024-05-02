import osmnx as ox
import networkx as nx
import folium

ox.settings.log_console=True
ox.settings.use_cache=True

# define the start and end locations in latlng
#Route made is from front of TSU to the library
#start_latlng = (37.78497,-122.43327)
#end_latlng = (37.78071,-122.41445)

def make_route(strt_lng ,strt_lat, end_lng, end_lt):

#For Debugging purposes the destination and starting point are hardset
    print("=================Make_Route Function Starting==========================")

    start_lat = float(33.87399)
    start_long = float(-117.92435)
    #end_latlng = (37.78071,-122.41445)
    end_lat = float(33.91732)
    end_long = float(-117.93312)

    # location where you want to find your route
    place     = 'Fullerton, California, United States'

    # find shortest route based on the mode of travel
    mode      = 'walk'        # 'drive', 'bike', 'walk'

    # find shortest path based on distance or time
    optimizer = 'length'        # 'length','time'

    # create graph from OSM within the boundaries of some
    # geocodable place(s)
    graph = ox.graph_from_place(place, network_type = mode, simplify=True, retain_all=False )
    orig_node = ox.nearest_nodes(graph, start_long,start_lat)
    dest_node = ox.nearest_nodes(graph, end_long,end_lat)


    #ox.bearing.add_edge_bearings(graph, precision=1)
    #Calculate Bearing Between two points, returns bearing in degrees
    #bearing = ox.bearing.calculate_bearing(lat1, lng1, lat2, lng2)
    shortest_route = ox.distance.shortest_path(graph,
                                      orig_node,
                                      dest_node,
                                      weight=optimizer)

    #creates a map viewable in HTML of set route
    route_map = ox.plot_route_folium(graph, shortest_route)
    route_map.save('route5.html')
    list_of_x = []
    list_of_y = []

    #Shortest_route is a list of nodeids, a node id can be converted into latitude and longitude
    #The following converts nodeids and saves lat and long to their own seperate list. 
    
    print("printing node ids.")
    for i in range(len(shortest_route)):
        curr_node = shortest_route[i]
        list_of_x.append(graph.nodes[curr_node]['x'])
        list_of_y.append(graph.nodes[curr_node]['y'])

    #print(*['Node #',, 'Node id', curr_node])
    print("Longitude",  list_of_x, sep="==>")
    print("Latitude", list_of_y, sep="==>")


    return shortest_route, list_of_x, list_of_y


