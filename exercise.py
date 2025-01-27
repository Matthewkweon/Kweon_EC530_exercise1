import math
import csv
import numpy as np
from scipy.spatial import cKDTree


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
    for curr_point in array1:
        lat1, lon1 = curr_point
        min_distance = float('inf')
        closest_coord = None

        for dest_point in array2:
            lat2, lon2 = dest_point
            dist = distance(lat1, lon1, lat2, lon2)
            if dist < min_distance:
                min_distance = dist
                closest_coord = [lat2, lon2]

        if closest_coord:
            results.append(closest_coord)
        else:
            results.append(None)

    return results


# AI GENERATED KDTREE ALGORITHM I FOUND. This was because my code kept crashing with the above implementation. 
def match_coords_kdtree(array1, array2):
    """
    Speed up matching by building a KD-Tree from array2.
    NOTE: This uses Euclidean distance on lat/lon in degrees (approximation).
    If your region is small, this is usually fine. 
    If you need global accuracy, see the notes above.
    """
    if not array2:
        return [None] * len(array1)

    # 1. Build a 2D KD-tree using lat, lon as if they're Cartesian.
    arr2_np = np.array(array2)  # shape: (m, 2)
    tree = cKDTree(arr2_np)     # Build the tree

    # 2. Convert array1 to numpy for vectorized queries
    arr1_np = np.array(array1)  # shape: (n, 2)

    # 3. Query all points in array1 at once for their nearest neighbor in array2
    #    'distances' will be the Euclidean distance in degrees,
    #    'indexes' will be the index in array2 of the nearest neighbor.
    distances, indexes = tree.query(arr1_np)  # shape: (n,)

    # 4. Reconstruct the matched points from array2
    results = []
    for idx in indexes:
        # idx is the row index in array2
        lat2, lon2 = array2[idx]
        results.append([lat2, lon2])
    
    return results

def parse_csv(filepath):
   
    possible_lng = ("lng", "long", "longitude")
    possible_lat = ("lat", "latitude")

    coords = []

    with open(filepath, mode='r', newline='', encoding='utf-8') as csv_file:
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
            raise ValueError("Unsupported CSV format. Required latitude and longitude columns not found.")
        for row in reader:
            try:
                lon = float(row[lng_col])
                lat = float(row[lat_col])
                coords.append([lat, lon])
            except ValueError:
                pass
                # print("skipping line")
    return coords


# current_location = parse_csv("test_2_curr.csv")
# print(current_location)
# dest_location = parse_csv("test_2_dest.csv")
# print(dest_location)


# curr_coords = [[42.349300, -71.106537]]
# dest_coords = parse_csv("test_1_dest.csv")

# result = match_coords(curr_coords, dest_coords)
# print(result)

# curr_coords = parse_csv("test_2_curr.csv")
# # print(curr_coords)
# dest_coords = parse_csv("test_2_dest.csv")
# # print(dest_coords)
# result = match_coords_kdtree(curr_coords, dest_coords)
# print(result)