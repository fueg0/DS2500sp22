####################
# Nicholas Fiorito
# DS2500 Homework 1
# 24 January 2022
# github.com/fueg0


# IMPORTS
import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from haversine import haversine as hs


# GLOBAL VARIABLES
station_df = pd.read_csv("stations.csv", columns=["Station ID", "Weather ID", "Lat", "Long"])
temp_df = pd.read_csv("temp.csv", columns=["Station ID", "Weather ID", "Month", "Day", "Temp"])
print(station_df)  # TODO: remove print
print(temp_df)  # TODO: remove print
fig, ax = plt.subplots()
fig2, bx = plt.subplots()


# FUNCTIONS

# float, float, float float -> float
# (lat, long), (lat,long) - > distance between points
def haversine(lat1, long1, lat2, long2):
    return hs(lat1, long1, lat2, long2)


# dataframe, distance function, float, float, float -> dataframe + distance column
def add_distance(dataframe, distance_fxn, lat, long, max_distance):
    df = dataframe.copy()
    filtered_df = df.drop(df.columns.difference(['Lat', 'Long']), 1, inplace=True)
    drop_indexes = []
    distances = []

    for index, row in filtered_df.iterrows():
        haversine_distance = distance_fxn(lat, long, row["Lat"], row["Long"])

        if haversine_distance > max_distance:
            drop_indexes.append(index)
        else:
            distances.append(haversine_distance)

    filtered_df.drop(labels=drop_indexes)
    filtered_df["Distance"] = distances
    print(filtered_df)  # TODO: remove print

    return filtered_df


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

