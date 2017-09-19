#!/usr/bin/env/python
"""
Title:
    Python script for 

Assumption:
    1. All the python packages are installed
    2. You are using python==2.7.11
    3. Any more assumptions <>

Description:
    1. Describe the class

Author:
    Abhijit Bansal

Copyright:
    (C) 2016 Faraday Future

"""
import googlemaps
from datetime import datetime

import math

from convert import calc_centre_lane
import polyline

gmaps = googlemaps.Client(key='AIzaSyCHDHUGzAhKsViuASECNblUNA69545Hr5Y')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("3165 Sawtelle Blvd, Los Angeles, CA 90066",
                                     "18455 S Figueroa St, Gardena, CA 90248",
                                     mode="driving",
                                     departure_time=now)

set_of_long_lat_1 = polyline.decode(directions_result[0]['overview_polyline']['points'])
cl_1 = calc_centre_lane(set_of_long_lat_1)

directions_result = gmaps.directions((34.024552, -118.445100), (34.028243, -118.442965), mode='walking')
set_of_long_lat_2 = polyline.decode(directions_result[0]['overview_polyline']['points'])
cl_2 = calc_centre_lane(set_of_long_lat_2)

