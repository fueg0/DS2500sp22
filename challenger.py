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


### GLOBAL VARIABLES
station_df = pd.read_csv("stations.csv", names=["stn", "Weather ID", "lat", "long"])
temp_df = pd.read_csv("temp.csv", names=["stn", "Weather ID", "month", "day", "temp"])
fig, ax = plt.subplots()
fig2, bx = plt.subplots()


### FUNCTIONS
# float, float, float float -> float
# TODO: info
def haversine(lat1, long1, lat2, long2):
    return float("{:0.3f}".format(hs((lat1, long1), (lat2, long2)))[:-1])


# dataframe, distance function, float, float, float -> dataframe + distance column
# TODO: info
def add_distance(dataframe, distance_fxn, lat, long, max_distance):
    df = dataframe.copy()
    filtered_df = df[df.columns[df.columns.isin(['stn', 'lat', 'long'])]]
    drop_indexes = []
    distances = []

    for index, row in filtered_df.iterrows():
        haversine_distance = distance_fxn(lat, long, row["lat"], row["long"])

        if haversine_distance > max_distance:
            drop_indexes.append(int(index))
        else:
            distances.append(haversine_distance)

    filtered_df = filtered_df.drop(labels=drop_indexes)
    filtered_df["Distance"] = distances

    return filtered_df


# float, float, float, float, float, float, float, float -> tuple (float, float)
# TODO: info
def convert_to_pos(start_lat, start_long, max_height, max_width, minlat, maxlat, minlong, maxlong):
    delta_long = maxlong - minlong
    delta_lat = maxlat - minlat

    lat_to_x = max_height * (1 - start_lat / delta_lat)
    long_to_y = max_width * (start_long / delta_long)

    return lat_to_x, long_to_y


###########
# Helper Functions
###########
# plot figure 1
def plot_first(dataframe):  # TODO: plot ax
    pass


# plot figure 2
def plot_second(dataframe):  # TODO: plot bx
    pass


# main
def main():
    station_cleaned = station_df.copy()
    temp_cleaned = temp_df.copy()

    station_cleaned.dropna(subset=["lat"], inplace=True)
    station_cleaned.dropna(subset=["long"], inplace=True)
    station_cleaned.dropna(subset=["stn"], inplace=True)
    print(station_cleaned.head(-1))

    temp_cleaned.dropna(subset=["stn"], inplace=True)
    print(temp_df.head(-1))

    cape_canaveral = (28.38823, -80.6243)
    within_range = add_distance(station_cleaned, haversine, cape_canaveral[0], cape_canaveral[1], 100)
    print(within_range)

    temp_cleaned = temp_cleaned[temp_cleaned["stn"].isin(within_range["stn"])]
    temp_cleaned = temp_cleaned[temp_cleaned["month"].isin([1])]
    temp_cleaned = temp_cleaned[temp_cleaned["day"] <= 27]
    print(temp_cleaned)

    plt.figure(1)
    plot_first(station_cleaned)
    plt.figure(2)
    plot_second(station_cleaned)

    exit(0)


if __name__ == '__main__':
    main()

