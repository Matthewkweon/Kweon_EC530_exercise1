# Mission of the module:  If the user gives you two arrays of geo location, match each point in the first array to the closest one in the second array
# Research and find the right formula for distance between two GPS locations.

import math
import csv

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

def parse_csv(filepath):

    possible_lng=("lng", "long", "longitude")
    possible_lat=("lat", "latitude")
    longitudes = []
    latitudes = []
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        normalized_fieldnames = [fn.lower() for fn in reader.fieldnames]
        
        lng_col = None
        lat_col = None
        
        for fn in reader.fieldnames:
            lower_fn = fn.lower()
            if lower_fn in possible_lng and lng_col is None:
                lng_col = fn
            if lower_fn in possible_lat and lat_col is None:
                lat_col = fn
        if not lng_col or not lat_col:
            raise ValueError(
                f"Could not find columns matching longitude keywords {possible_lng} "
                f"and latitude keywords {possible_lat} in CSV headers {reader.fieldnames}."
            )
        for row in reader:
            try:
                lon = float(row[lng_col])
                lat = float(row[lat_col])
                longitudes.append(lon)
                latitudes.append(lat)
            except ValueError:
                print(f"Skipping row with invalid longitude/latitude values: {row}")
    
    return longitudes, latitudes
