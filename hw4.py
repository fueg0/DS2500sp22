#################################
# Nicholas Fiorito
# 11 February 2022
# github.com/fueg0, all work shown is my own unless a source is commented

# IMPORTS
import numpy as np
import pandas as pd


# GLOBAL VARIABLES
bike_df = pd.read_csv("bike_data.csv")
traffic_df = pd.read_csv("Traffic_Counts_-_Hourlyp0042.csv")


# FUNCTIONS
# takes in a dataframe two column names and a function to create the third column name with
# returns a dataframe with the new column
def combine_columns(df, col1, col2, process, col3):
    new_col = []

    for col1_data, col2_data in df[col1], df[col2]:
        new_data = process(col1_data, col2_data)
        new_col.append(new_data)

    df[col3] = new_col
    return df


def average_volume_at_hour(hour, dict):
    volume = 0
    counter = 0
    for info in dict.values():
        try:
            date_volume = info[hour]
            volume += date_volume
            counter += 1

        except KeyError as e:
            pass

    return volume / counter

# MAIN
def main():
    bike_df_main = bike_df.copy()
    bike_df_main = bike_df_main[bike_df_main.columns[bike_df_main.columns.isin(["Day of the Week", "Working Day"])]]

    traffic_df_main = traffic_df.copy()
    traffic_df_main = traffic_df_main.drop(["DateTime", "DateTime2", "Sta_Dir", "OBJECTID", "ABPair", "DateTimeTxt"],
                                           axis=1)
    date_col = []
    hour_col = []

    for item in traffic_df_main["DateTime1"]:
        date_hour = item.split()
        date_col.append(date_hour[0])
        hour_col.append(date_hour[1][:2])

    traffic_df_main["Date"] = date_col
    traffic_df_main["Hour"] = hour_col

    # Honestly I can't figure out how groupby works. I'll just do it by hand
    rebuild_csv = {}
    for index, row in traffic_df_main.iterrows():
        if row["Date"] not in rebuild_csv.keys():
            rebuild_csv[row["Date"]] = {row["Hour"]: row["Volume"]}
        else:
            if row["Hour"] not in rebuild_csv[row["Date"]].keys():
                rebuild_csv[row["Date"]][row["Hour"]] = row["Volume"]
            else:
                rebuild_csv[row["Date"]][row["Hour"]] = rebuild_csv[row["Date"]][row["Hour"]] + row["Volume"]

    print(rebuild_csv)

    # How much traffic is there on average at 8am?
    print("The average volume of traffic at 8am is %d\n" % average_volume_at_hour("08", rebuild_csv))

    # How much traffic is there on average at 3am?
    print("The average volume of traffic at 3am is %d\n" % average_volume_at_hour("03", rebuild_csv))

    # Find out the hour of day with the highest average traffic and the hour of day with the lowest average traffic.
    times = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

    time_to_volume = {}

    for hour in times:
        avg_volume = average_volume_at_hour(hour, rebuild_csv)
        time_to_volume[hour] = avg_volume

    highest_traffic = max(time_to_volume.values())
    lowest_traffic = min(time_to_volume.values())
    time_to_volume.keys()[time_to_volume.values().index(highest_traffic)]
    time_to_volume.keys()[time_to_volume.values().index(lowest_traffic)]


# DRIVER
if __name__ == "__main__":
    main()
