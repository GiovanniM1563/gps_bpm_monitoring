import GPSUtil



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


while True:
    test_gps_readout()

    
