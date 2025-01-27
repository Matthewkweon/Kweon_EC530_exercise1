# EXERCISE 1 for EC530
## By: Yongjoon Kweon

In this exercise, I created an exercise.py file that contains my functions that calculate the distance between two geographical coordinates. I also created a function that will match each coordinate in the first array to the coordinate with the smallest distance in the second array.

I matched each coordinate with another coordinate that it was closest to. I also created a scripting file that would test my outputs. I first tested my distance function, then I tested my matching function next. 

First of all, I only support the following input formats:
- Raw Lists of Lists
    - E.g., [[42.349300, -71.106537], [42.34857, -71.10689], ...]
    - Passed directly to match_coords or match_coords_kdtree.

- CSV Files (via parse_csv)
    - Must contain columns labeled in any of these ways:
    - Latitude column name: lat or latitude
    - Longitude column name: lng, long, or longitude
    - Example headers that work: Latitude, Longitude or lat, long etc.
    - If the CSV file doesn’t contain at least one matching latitude and longitude column, the parser raises a ValueError with a message like:
        - "Unsupported CSV format. Required columns not found."



Thought about README for CSV Parsing
Below is a sample README that you can include alongside your code. Simply copy this into a file named README.md (or adapt as desired) to provide helpful instructions for anyone who wants to use or test your script.

Coordinate Matching Utilities
This repository contains Python utilities for:

Distance Calculation

Calculates the distance (in km) between two latitude/longitude coordinates using the Haversine formula.
Coordinate Matching

Matches each point in one list of coordinates with the closest point in another list of coordinates.
Provides two different matching approaches:
Brute Force (match_coords)
KD-Tree Based (match_coords_kdtree) for more efficient lookups on larger datasets.
CSV Parsing

Parses CSV files that contain latitude and longitude columns (recognized labels: lat, latitude, lng, long, longitude).
Returns a list of coordinate pairs in the format [[lat1, lon1], [lat2, lon2], ...].
Supported Input Formats
Raw Lists of Lists

E.g., [[42.349300, -71.106537], [42.34857, -71.10689], ...]
Passed directly to match_coords or match_coords_kdtree.
CSV Files (via parse_csv)

Must contain columns labeled in any of these ways:
Latitude column name: lat or latitude
Longitude column name: lng, long, or longitude
Example headers that work: Latitude, Longitude or lat, long etc.
If the CSV file doesn’t contain at least one matching latitude and longitude column, the parser raises a ValueError with a message like:
"Unsupported CSV format. Required columns not found."

Installation and Requirements
- Python 3.8+ recommended
- Dependencies: numpy, scipy (for KD-Tree usage)
- (Optionally) install pytest if you’d like to run tests.

To install dependencies, run:

pip install numpy scipy pytest


To test the code, you must following steps:
- input a test case into my pytest file named "test_exercise.py"
    - you may want to comment out my test cases right now
- Be sure that your csv file contains keywords "latitude, lat" or "longitude, long, lng"
- Place the .csv file in the codebase (such as other .csv files already there like test_1_curr.csv)
- Write out a test function in my python script to test whatever you want to test. (Or do it in the exercise.py file, it doesn't matter)
- Run: "pytest"
    - You can run "pytest -s" for more detailed answers and even "pytest -s > output.txt" to get the output in a .txt file

Here is an example of how to format your test functions and testing. 
```bash
import math
import numpy as np
from exercise import distance, match_coords, match_coords_kdtree, parse_csv

# 1. Use raw lists of lists (latitude, longitude) pairs:
array1 = [
    [42.349300, -71.106537],
    [45.0000, -75.0000]
]
array2 = [
    [42.34857, -71.10689],
    [45.0001, -75.0001]
]

# Brute force matching
matched_brute = match_coords(array1, array2)
print("Brute Force Matching:", matched_brute)



Scenario 2:

# KD-Tree based matching (faster for large datasets and .csv files)
coords_from_csv = parse_csv("my_coords.csv")
print("CSV coordinates:", coords_from_csv)

# Then you can match:
another_dataset = [[42.3500, -71.1070], [45.0100, -75.0050]]
result = match_coords(coords_from_csv, another_dataset)
print("Matched from CSV:", result)
```