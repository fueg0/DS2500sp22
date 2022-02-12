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
    bike_df_main = bike_df_main[bike_df_main.columns[bike_df_main.columns.isin(["Date", "Working Day"])]]

    traffic_df_main = traffic_df.copy()
    traffic_df_main = traffic_df_main.drop(["DateTime", "DateTime2", "Sta_Dir", "OBJECTID", "ABPair", "DateTimeTxt"],
                                           axis=1)
    bike_df_main = bike_df_main[bike_df_main["Working Day"] == 1]
    bike_df_main = bike_df_main.drop_duplicates(subset=["Date"], keep='last')
    bike_dates = []
    for date in bike_df_main["Date"]:
        if len(date.split("/")[0]) == 1:
            bike_dates.append(str("0%s" % date))
        else:
            bike_dates.append(date)

    bike_df_main["Date"] = bike_dates

    date_col = []
    hour_col = []
    for item in traffic_df_main["DateTime1"]:
        date_hour = item.split()
        date_col.append(date_hour[0])
        hour_col.append(date_hour[1][:2])

    traffic_df_main["Date"] = date_col
    traffic_df_main["Hour"] = hour_col

    # Part 2

    # Honestly I can't figure out how groupby works. I'll just do it by hand
    # because it'll be faster than dealing with matoplotlib documentation.
    rebuild_csv = {}
    for index, row in traffic_df_main.iterrows():
        if row["Date"] not in rebuild_csv.keys():
            rebuild_csv[row["Date"]] = {row["Hour"]: row["Volume"]}
        else:
            if row["Hour"] not in rebuild_csv[row["Date"]].keys():
                rebuild_csv[row["Date"]][row["Hour"]] = row["Volume"]
            else:
                rebuild_csv[row["Date"]][row["Hour"]] = rebuild_csv[row["Date"]][row["Hour"]] + row["Volume"]

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

    # highest/lowest traffic
    highest_traffic = max(time_to_volume.values())
    lowest_traffic = min(time_to_volume.values())
    # highest/lowest traffic hour
    highest_traffic_hour = list(time_to_volume.keys())[list(time_to_volume.values()).index(highest_traffic)]
    lowest_traffic_hour = list(time_to_volume.keys())[list(time_to_volume.values()).index(lowest_traffic)]
    # print highest/lowest traffic
    print("the hour of day with the highest average traffic is %s with a volume of %s\n" % (round(highest_traffic), highest_traffic_hour))
    print("the hour of day with the lowest average traffic is %s with a volume of %s\n" % (round(lowest_traffic), lowest_traffic_hour))

    # Compare the total traffic on two dates from 2011: March 27th and April 22nd
    for date in rebuild_csv.keys():
        if date == "03/27/2011" or date == "04/22/2011":
            volume = sum(rebuild_csv[date].values())
            print("The total volume of traffic on %s was %d\n" % (date, volume))

    # How much traffic is there on an average July day?
    traffic_df_copy = traffic_df_main.copy()
    month_col = []
    for date in traffic_df_copy["Date"]:
        month_col.append(date[:2])
    traffic_df_copy["Month"] = month_col
    traffic_df_copy = traffic_df_copy[traffic_df_copy["Month"] == "07"]
    average_traffic_volume_july = sum(traffic_df_copy["Volume"]) / len(traffic_df_copy["Volume"])
    print("The average traffic on a July day is %d cars\n" % round(average_traffic_volume_july))

    # How much traffic is there on an average workday (this is merged in from the Bike data)?
    volume = []
    length = 0
    for date in rebuild_csv.keys():
        if date in bike_df_main["Date"].values:
            volume.append(sum(rebuild_csv[date].values()))
            length += 1
    print("The average amount of traffic on a workday is %d cars\n" % round(sum(volume) / length))


# DRIVER
if __name__ == "__main__":
    main()
    exit()
