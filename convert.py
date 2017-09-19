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
from math import radians, cos, sin, asin, sqrt, atan2, degrees


def calculate_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    credit - Michael Dunn
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def calculate_bearing(long1, lat1, long2, lat2):
    """Returns bearing in degrees"""
    bearing = atan2(sin(long2 - long1) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(long2 - long1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360
    return bearing


def calc_centre_lane(points):
    centre_lane = [(0, 0)]
    for idx, point in enumerate(points[1:], 1):
        curr_long, curr_lat = point
        prev_long, prev_lat = points[idx - 1]

        dist = calculate_distance(prev_long, prev_lat, curr_long, curr_lat)
        bearing = calculate_bearing(prev_long, prev_lat, curr_long, curr_lat)

        prev_x, prev_y = centre_lane[idx - 1]

        curr_x = prev_x + (cos(radians(bearing)) * dist)
        curr_y = prev_y + (sin(radians(bearing)) * dist)

        centre_lane.append((curr_x, curr_y))
    return centre_lane