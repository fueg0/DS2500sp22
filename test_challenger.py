'''
    test_challenger.py
    DS2500
    Spring 2022
    Test suite for HW #2

    We don't yet need to know exactly how to create unit tests like these,
   but in this homework we'll get some practice with using them.

   For each function described in the HW, this piece of code will
   create a couple of sample inputs and expected outputs. Doe the function,
   given those sample inputs, create the expected outputs? If so, great!

   Output that means all is good: "Ran 3 tests in 0.001s...OK" or similar

   Output that means something is wrong: "FAIL: test_add_distance"
   In case of a fail, it'll telll you what the expected vs actual outputs
   were.
'''

import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
import numpy as np
from challenger import add_distance, haversine, convert_to_pos


class TestChallenger(unittest.TestCase):
    def test_add_distance(self):
        # Add distance from my house to station/long/lat columns
        start_data = [[1, 50.05, 5.4253]]
        start = pd.DataFrame(start_data, columns=["stn", "lat", "long"])

        actual = add_distance(start, haversine, 42.3022, -71.0568, 7000)
        actual = actual.values.tolist()

        end = [[1, 50.05, 5.4253, 5690.2071]]
        np.testing.assert_almost_equal(actual, end, decimal=2)

        # Add distance from 0.0,0.0 to station/long/lat columns
        start_data = [[1, 3.4, 5.5], [2, 15.5, 17.8]]
        start = pd.DataFrame(start_data, columns=["stn", "lat", "long"])

        actual = add_distance(start, haversine, 0.0, 0.0, 7000)
        actual = actual.values.tolist()

        end = [[1, 3.4, 5.5, 718.688], [2, 15.5, 17.8, 2606.0288]]
        np.testing.assert_almost_equal(actual, end, decimal=2)

        # Same as above but one is over the threshold
        start_data = [[1, 3.4, 5.5], [2, 15.5, 17.8]]
        start = pd.DataFrame(start_data, columns=["stn", "lat", "long"])

        actual = add_distance(start, haversine, 0.0, 0.0, 1000)
        actual = actual.values.tolist()

        end = [[1, 3.4, 5.5, 718.688]]
        np.testing.assert_almost_equal(actual, end, decimal=2)

    def test_haversine(self):
        # Distance between Big Ben and the statue of liberty
        self.assertAlmostEqual(haversine(51.5007, .1246, 40.6892, 74.0445),
                               5574.84, 2)

        # Distance between my house and Northeastern
        self.assertAlmostEqual(haversine(42.3022, -71.0568, 42.3218, -71.1084),
                               4.77, 2)

    def test_convert_to_pos(self):
        xsize = 100
        ysize = 100
        latmin = 0
        latmax = 50
        longmin = 0
        longmax = 50

        # First test: 0, 0 should be in the bottom-left corner
        start_lat = 0.0
        start_long = 0.0
        expected = (100, 0)
        actual = convert_to_pos(start_lat, start_long, xsize, ysize,
                                latmin, latmax, longmin, longmax)
        self.assertEqual(actual, expected)

        # Second test: 50, 50 should be in the top-right corner
        start_lat = 50.0
        start_long = 50.0
        expected = (0, 100)
        actual = convert_to_pos(start_lat, start_long, xsize, ysize,
                                latmin, latmax, longmin, longmax)
        self.assertEqual(actual, expected)

        # Second test: 25, 30 should be in the middle-ish
        start_lat = 25
        start_long = 30
        expected = (50, 60)
        actual = convert_to_pos(start_lat, start_long, xsize, ysize,
                                latmin, latmax, longmin, longmax)
        self.assertEqual(actual, expected)


def main():
    unittest.main(verbosity=3)


main()

