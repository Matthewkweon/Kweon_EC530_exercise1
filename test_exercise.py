import math
import pytest
from unittest.mock import patch, mock_open
from exercise import distance, match_coords, parse_csv, match_coords_kdtree

def test_distance():
    lat1, long1 = 50.32873, -47.2363
    lat2, long2 = 77.38232, -99.8732
    dist = distance(lat1, long1, lat2, long2)
    # Expected results: About 3701
    assert 3700 <= dist <= 3705,f"Distance {dist} km is WRONG"
    print(dist)


def test_matching():
    array1 = [[0, 0],[20, 20], [79, 99]]
    array2 = [[3, 3],[15, 15],[100, 100]]
    # Expected results:
    # (0,0) -> (3,3)
    # (20,20) -> (15,15)
    # (79,99) -> (100,100)
    expected = [[3, 3], [15, 15], [100,100]]

    result = match_coords(array1, array2)
    assert result == expected, f"Expected {expected}, got {result}"
    print(result)


def test_parse_csv():
    current_location = parse_csv("test_2_curr.csv")
    print(current_location)


def test_1():
    curr_coords = [[42.349300, -71.106537]]
    dest_coords = parse_csv("test_1_dest.csv")

    result = match_coords(curr_coords, dest_coords)

    expected = [[42.348569930505455, -71.10689247607672]]

    assert result == expected, f"Expected {expected}, got {result}"
    # print(result)


def test_2():
    curr_coords = parse_csv("test_2_curr.csv")
    dest_coords = parse_csv("test_2_dest.csv")

    result = match_coords_kdtree(curr_coords, dest_coords)
    # print(result)


@pytest.mark.xfail(reason="We expect this to fail due to incorrect CSV format")
def test_3():
    curr_coords = parse_csv("test_3_curr.csv")
    
    # Should fail because the Cities excel format and not in longitude and latitude format, the Current
    # Cities .csv file isn't correct in its format


def test_4():
    curr_coords = parse_csv("test_2_curr.csv")
    dest_coords = parse_csv("test_4_dest.csv")

    result = match_coords_kdtree(curr_coords, dest_coords)

@pytest.mark.xfail(reason="We expect this to fail due to incorrect CSV format")
def test_no_dest_arr():
    curr_coords = parse_csv("test_2_curr.csv")


@pytest.mark.xfail(reason="We expect this to fail due to incorrect CSV format")
def test_north_south():
    expected = [["47.5", "68.5"]]
    actual = parse_csv(["47.5 E", "68.5 E"])
