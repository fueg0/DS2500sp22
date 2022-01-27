'''
    DS2500
    Spring 2022
    HW1 test suite

    We don't yet need to know exactly how to create unit tests like these,
    but in this homework we'll get some practice with using them.

    For each function described in the HW, this piece of code will
    create a couple of sample inputs and expected outputs. Doe the function,
    given those sample inputs, create the expected outputs? If so, great!

    Output that means all is good: "Ran 3 tests in 0.001s" or similar

    Output that means something is wrong: "FAIL: test_transform_hockey"
    In case of a fail, it'll telll you what the expected vs actual outputs
    were.
'''

import unittest
from husky_results import transform_hockey, clean_data, max_nested


class TestHockey(unittest.TestCase):
    def test_transform_hockey(self):
        self.assertEqual(transform_hockey([], 0), {})

        lst = [["date", "opponent"], ["1/1", "BU"]]
        dct = {"1/1": {"opponent": "BU"}}
        self.assertEqual(transform_hockey(lst, 0), dct)

        lst = [["opponent", "date"], ["BU", "1/1"], ["HC", "1/2"]]
        dct = {"1/1": {"opponent": "BU"},
               "1/2": {"opponent": "HC"}}
        self.assertEqual(transform_hockey(lst, 1), dct)

        lst = [["opponent", "date", "P"], ["BU", "1/1", "3"],
               ["HC", "1/2", "4"], ["BC", "1/5", "8"]]
        dct = {"1/1": {"opponent": "BU", "P": "3"},
               "1/2": {"opponent": "HC", "P": "4"},
               "1/5": {"opponent": "BC", "P": "8"}}
        self.assertEqual(transform_hockey(lst, 1), dct)

    def test_clean_data(self):
        start = {"1/1": {"opponent": "BU"}}
        self.assertEqual(clean_data(start, ["opponent"]), start)

        start = {"1/1": {"opponent": "BU", "P": "3"},
                 "1/2": {"opponent": "HC", "P": "4"},
                 "1/5": {"opponent": "BC", "P": "8"}}
        expected = {"1/1": {"P": 3},
                    "1/2": {"P": 4},
                    "1/5": {"P": 8}}

        self.assertEqual(clean_data(start, ["P"]), expected)

        start = {"1/1": {"opponent": "BU", "P": "3", "PP": "0"},
                 "1/2": {"opponent": "HC", "P": "4", "PP": "1"},
                 "1/5": {"opponent": "BC", "P": "8", "PP": "0"}}
        expected = {"1/1": {"opponent": "BU", "PP": 0},
                    "1/2": {"opponent": "HC", "PP": 1},
                    "1/5": {"opponent": "BC", "PP": 0}}

        self.assertEqual(clean_data(start, ["opponent", "PP"]), expected)

    def test_max_nested(self):
        start = {"1/1": {"X": 10}}
        expected = ("1/1", 10)
        self.assertEqual(max_nested(start, "X"), expected)

        start = {"1/1": {"X": 10}, "1/2": {"X": 11}}
        expected = ("1/2", 11)
        self.assertEqual(max_nested(start, "X"), expected)

        start = {"1/1": {"X": 10, "Y": 0}, "1/2": {"X": 11, "Y": 1},
                 "1/3": {"X": 10, "Y": 0, "Z": 18}}
        expected = ("1/2", 1)
        self.assertEqual(max_nested(start, "Y"), expected)


def main():
    unittest.main(verbosity=3)


main()
