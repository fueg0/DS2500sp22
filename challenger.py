####################
# Nicholas Fiorito
# DS2500 Homework 1
# 24 January 2022
# github.com/fueg0


# IMPORTS
import csv
import math
import numpy as np
import pandas
import matplotlib.pyplot as plt
from haversine import haversine as hs


# GLOBAL VARIABLES
fig, ax = plt.subplots()
fig2, bx = plt.subplots()


# FUNCTIONS

# float, float, float float -> float
# (lat, long), (lat,long) - > distance between points
def haversine(lat1, long1, lat2, long2):
    return hs(lat1, long1, lat2, long2)


# pass file to csv_to_2DList, append header array at index 0,
# 2DList to array of dict. loop through array. For index in list,
# feed lat and long keys plus lat+long args into distance_fxn.
# if output is under
# dataframe, distance function, float, float, float -> dataframe + distance column
def add_distance(dataframe, distance_fxn, lat, long, max_distance):



#
def convert_to_pos(start_lat, start_long, max_height, max_width, lat1, long1, lat2, long2):
    pass


###########
# Helper Functions
###########
# Turns a CSV into a lists of string arrays, where each string array represents a line from the csv file
### I know python functions shouldn't have numbers in their name, but it's the most accurate name
def csv_to_2DList(filename):
    file = []

    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)

        for row in csv_reader:
            # print(row) # this was just for data output visualization on my end to make sure my dictionaries were right
            file.append(row)

    return file


# plot figure 1
def plot_first(x):  # TODO: plot ax
    pass


# plot figure 2
def plot_second(x):  # TODO: plot bx
    pass


# main
def main():
    cleaned_for_goals = 5
    cleaned_for_plot = 6

    plt.figure(1)
    plot_first(cleaned_for_goals)
    plt.figure(2)
    plot_second(cleaned_for_plot)
    plt.show()

    exit(0)


if __name__ == '__main__':
    main()

