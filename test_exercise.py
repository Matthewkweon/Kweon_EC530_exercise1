import math
import pytest
from exercise import distance, match_coords

def test_distance():
    lat1, long1 = 50.32873, -47.2363
    lat2, long2 = 77.38232, -99.8732
    dist = distance(lat1, long1, lat2, long2)
    # Expected results: About 3701
    assert 3700 <= dist <= 3705,f"Distance {dist} km is WRONG"


def test_matching():
    array1 = [(0, 0),(20, 20), (79, 99)]
    array2 = [(3, 3),(15, 15),(100, 100)]
    # Expected results:
    # (0,0) -> (3,3)
    # (20,20) -> (15,15)
    # (79,99) -> (100,100)
    expected = [(3, 3), (15, 15), (100,100)]

    result = match_coords(array1, array2)
    assert result == expected, f"Expected {expected}, got {result}"
