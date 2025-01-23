# Mission of the module:  If the user gives you two arrays of geo location, match each point in the first array to the closest one in the second array
# Research and find the right formula for distance between two GPS locations.

import math

def distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad = math.radians(lat1)
    long1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    long2_rad = math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_long = long2_rad - long1_rad


    a = (math.sin(delta_lat / 2))**2 + \
    math.cos(lat1_rad) * math.cos(lat2_rad) \
    * (math.sin(delta_long / 2))**2

    c = 2* math.asin(math.sqrt(a))
    d = R * c
    return d

def match_coords(array1, array2):
    results = []

    for u,v in array1:
        min_distance = float('inf')
        min_coord = (0,0)
        for w,x in array2:
            temp_dist = distance(u,v,w,x)
            if temp_dist < min_distance:
                min_distance = temp_dist
                min_coord = (w,x)
        if array2:
            results.append(min_coord)
    return results