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


# MAIN
def main():
    traffic_df_main = traffic_df.copy()
    traffic_df_main = combine_columns(traffic_df_main, )


# DRIVER
if __name__ == "__main__":
    pass
