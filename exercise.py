import math
import csv
import numpy as np
from scipy.spatial import cKDTree
import logging

# 1) Import the JSON logger utilities from your separate file
from event_logging import get_json_logger, track_event

# 2) Create a logger instance for this module (using the JSON formatter)
logger = get_json_logger(__name__, level=logging.DEBUG)

def distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance (in kilometers) between two points
    on the Earth (specified in decimal degrees).
    """
    # Log event at the start, with context
    track_event(logger, "Distance_Start", {
        "lat1": lat1, "lon1": lon1,
        "lat2": lat2, "lon2": lon2
    }, level=logging.DEBUG)

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

    c = 2 * math.asin(math.sqrt(a))
    d = R * c

    # Log event at the end, providing the result
    track_event(logger, "Distance_End", {
        "distance_km": d
    }, level=logging.DEBUG)
    return d

def match_coords(array1, array2):
    """
    Brute force matching: For each point in array1, find the closest point in array2.
    """
    track_event(logger, "MatchCoords_Start", {
        "num_array1": len(array1),
        "num_array2": len(array2)
    })

    results = []
    for i, curr_point in enumerate(array1, start=1):
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
            # Log an event if we found a closest coordinate
            track_event(logger, "MatchCoords_Matched", {
                "index": i,
                "source_coord": curr_point,
                "closest_coord": closest_coord,
                "distance_km": min_distance
            }, level=logging.DEBUG)
        else:
            # Optionally handle no-match scenario
            # results.append(None)
            track_event(logger, "MatchCoords_NoMatch", {
                "index": i,
                "source_coord": curr_point
            }, level=logging.WARNING)

    track_event(logger, "MatchCoords_End")
    return results

def match_coords_kdtree(array1, array2):
    """
    Speed up matching by building a KD-Tree from array2.
    NOTE: This uses Euclidean distance on lat/lon in degrees (approximation).
    If your region is small, this is usually fine.
    If you need global accuracy, see the notes above.
    """
    track_event(logger, "MatchCoordsKDTree_Start", {
        "num_array1": len(array1),
        "num_array2": len(array2)
    })

    if not array2:
        track_event(logger, "MatchCoordsKDTree_EmptyDestination", {
            "reason": "Destination array is empty"
        }, level=logging.WARNING)
        return [None] * len(array1)

    arr2_np = np.array(array2)  # shape: (m, 2)
    tree = cKDTree(arr2_np)

    arr1_np = np.array(array1)  # shape: (n, 2)
    distances, indexes = tree.query(arr1_np)

    results = []
    for idx, (dist, src_point) in enumerate(zip(distances, arr1_np), start=1):
        lat2, lon2 = array2[indexes[idx - 1]]
        results.append([lat2, lon2])
        track_event(logger, "MatchCoordsKDTree_Matched", {
            "index": idx,
            "source_coord": src_point.tolist(),
            "matched_coord": [lat2, lon2],
            "euclidean_dist_degrees": float(dist)
        }, level=logging.DEBUG)

    track_event(logger, "MatchCoordsKDTree_End")
    return results

def parse_csv(filepath):
    """
    Parses a CSV file and returns a list of [lat, lon] coordinates.
    """
    track_event(logger, "ParseCSV_Start", {"filepath": filepath})

    possible_lng = ("lng", "long", "longitude")
    possible_lat = ("lat", "latitude")

    coords = []

    with open(filepath, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames:
            track_event(logger, "ParseCSV_NoHeader", {
                "message": "CSV has no header row or is empty.",
                "filepath": filepath
            }, level=logging.ERROR)
            return coords

        lng_col = None
        lat_col = None
        for fn in reader.fieldnames:
            lower_fn = fn.lower()
            if lower_fn in possible_lng and lng_col is None:
                lng_col = fn
            if lower_fn in possible_lat and lat_col is None:
                lat_col = fn

        if not lng_col or not lat_col:
            track_event(logger, "ParseCSV_MissingColumns", {
                "message": "No latitude/longitude columns found.",
                "filepath": filepath
            }, level=logging.ERROR)
            raise ValueError("Required latitude/longitude columns not found in CSV.")

        for row_number, row in enumerate(reader, start=1):
            try:
                lon = float(row[lng_col])
                lat = float(row[lat_col])
                coords.append([lat, lon])
            except ValueError:
                track_event(logger, "ParseCSV_InvalidRow", {
                    "row_number": row_number,
                    "row_content": row
                }, level=logging.WARNING)

    track_event(logger, "ParseCSV_End", {
        "filepath": filepath,
        "num_coords": len(coords)
    })
    return coords

