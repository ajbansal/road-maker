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

"""
import googlemaps
from datetime import datetime

import math

import os

import road_lib

from convert import calc_centre_lane
import polyline

gmaps = googlemaps.Client(key=os.environ.get('API_Key'))

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("3165 Sawtelle Blvd, Los Angeles, CA 90066",
                                     "3200 Zanker Road, San Jose, CA",
                                     mode="driving",
                                     departure_time=now)

set_of_long_lat_1 = polyline.decode(directions_result[0]['overview_polyline']['points'])
cl_1 = calc_centre_lane(set_of_long_lat_1)
road = road_lib.read_road(cl_1)
road_lib.plot_road(road.coordinates, cl_1, scatter=False)

directions_result = gmaps.directions((34.049235, -118.460729), (34.015948, -118.430239), mode='walking')
set_of_long_lat_2 = polyline.decode(directions_result[0]['overview_polyline']['points'])
cl_2 = calc_centre_lane(set_of_long_lat_2)
road_2 = road_lib.read_road(cl_2)
road_lib.plot_road(road_2.coordinates, cl_2, scatter=False)



