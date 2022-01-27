####################
# Nicholas Fiorito
# DS2500 Homework 1
# 24 January 2022
# github.com/fueg0

# IMPORTS
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# GLOBAL VARIABLES
fig, ax = plt.subplots()
fig2, bx = plt.subplots()


# FUNCTIONS
# Function 1- 2DList of String, int -> Dict
def transform_hockey(string_list, column):
    hockey_transformed_dict = {}
    if len(string_list) > 1:
        try:
            labels = string_list[0]
            data = string_list[1:]

            for game in data:
                date = game[column]
                hockey_transformed_dict[date] = double_list_to_dict(game, labels)

            hockey_transformed_dict = remove_keys(hockey_transformed_dict, ['date'])
            return hockey_transformed_dict
        except Exception as e:
            print(e)
            print("something broke with the inputs in transform_hockey")
    else:
        return {}


# Function 2- Dict of Dict, list of string -> Dict of String
def clean_data(nested_dict, selected_fields):
    nested_dict = remove_keys(nested_dict, selected_fields, keep=True)

    # make sure types are correct
    for keys, values in nested_dict.items():
        for nested_key in values:
            # Dynamic type-casting, if string CAN BE CAST to int then cast, else pass on exception and leave un-cast
            # from https://stackoverflow.com/questions/8075877/converting-string-to-int-using-try-except-in-python/8075959
            try:
                nested_dict[keys][nested_key] = int(nested_dict[keys][nested_key])
            except ValueError:
                # ignore the exception, leave string intact
                pass

    return nested_dict


# Function 3- Dict of Dict, string -> Tuple
def max_nested(nested_dict, selected_field):
    field_values = {}

    for key, value in nested_dict.items():
        field_value = value.get(selected_field)
        field_values[field_value] = key

    maximum = max(field_values.keys())

    return field_values[maximum], maximum


###########
# Helper Functions
###########
# Turns the two lists supplied into a dictionary keyed by the contents of fields
def double_list_to_dict(values, keys):
    return_dict = {}

    for i in range(len(keys)):
        return_dict[keys[i]] = values[i]

    return return_dict


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


# Removes all keys from a nested dictionary, changing keep to True keeps only the given keys
def remove_keys(nested_dict, keys_to_remove, keep=False):
    for keys, values in nested_dict.items():
        if keep:
            # modified the stackoverflow solution for both inclusion and exclusion of $keys_to_remove
            final_dict = {key: values[key] for key in values if key in keys_to_remove}
        else:
            # acquired this very slick dictionary comprehension from:
            # https://stackoverflow.com/questions/8995611/removing-multiple-keys-from-a-dictionary-safely
            final_dict = {key: values[key] for key in values if key not in keys_to_remove}

        nested_dict[keys] = final_dict

    return nested_dict


###########
# Answering HW Questions
###########

# Set Variables
file_data = csv_to_2DList("huskies_hockey_stats.csv")

hockey_dict = transform_hockey(file_data, 1)

cleaned_data = clean_data(hockey_dict, ["Opponent", "W/L", "G", "A", "PP", "BLK"])


# Perform Operations:
##########
# On what date did we: score the most goals?
#
max_goals = -1
max_goals_date = "0/0/0"
for goals_key, goal_values in cleaned_data.items():
    if goal_values["G"] > max_goals:
        max_goals = goal_values["G"]
        max_goals_date = goals_key
print("--------------------------")
print("We scored the most goals (%d goals!) on %s\n" % (max_goals, max_goals_date))

##########
# On what date did we: have the most assists?
#
max_assists = -1
max_assists_date = "0/0/0"
for assist_key, assist_values in cleaned_data.items():
    if assist_values["A"] > max_assists:
        max_assists = assist_values["A"]
        max_assists_date = assist_key
print("--------------------------")
print("We got the most assists (%d assists!) on %s\n" % (max_assists, max_assists_date))

##########
# On what date did we: block the most shots?
#
max_blocks = -1
max_blocks_date = "0/0/0"
for block_key, block_values in cleaned_data.items():
    if block_values["BLK"] > max_blocks:
        max_blocks = block_values["BLK"]
        max_blocks_date = block_key
print("--------------------------")
print("We got the most blocks (%d blocks!) on %s\n" % (max_blocks, max_blocks_date))

##########
# On how many dates did we: win?
#
win_counter = 0
for win_key, win_values in cleaned_data.items():
    if win_values["W/L"] == "W":
        win_counter += 1
print("--------------------------")
print("We won on %d dates this year!\n" % win_counter)

##########
# On how many dates did we: have exactly one power play?
#
pp_counter = 0
for pp_key, pp_values in cleaned_data.items():
    if pp_values["PP"] == 1:
        pp_counter += 1
print("--------------------------")
print("We had exactly one power play on %d dates this year!\n" % pp_counter)


###########
# HW Visualizations
###########
# A histogram showing the number of games in which we scored 0, 1..., n goals.
def plot_first(data):
    all_goals = []
    plt.title("Goal Scoring Frequencies from Northeastern Women's Hockey")
    plt.xlabel("Number of Goals Scored")
    plt.ylabel("Number of Times This Many Goals Was Scored")
    plt.grid(visible=True, alpha=0.5)

    for goal_data in data.values():
        for goal_count in goal_data.values():
            all_goals.append(goal_count)

    # https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
    mode_goal = Counter(all_goals).most_common(1)[0][1]

    ax.set(xlim=(0, max_goals), xticks=np.arange(0, (max_goals + 2)),
           ylim=(0, mode_goal), yticks=np.arange(0, mode_goal, 2))

    ax.hist(all_goals, bins=(max_goals + 1), align='mid', range=[0, (max_goals + 1)], linewidth=0.5, edgecolor="black")


# A scatter plot of shots blocked on the x-axis vs. assists on the y-axis.
def plot_second(data):
    plt.title("Shots Blocked vs. Assists from Northeastern Women's Hockey")
    plt.xlabel("Shots Blocked in Game")
    plt.ylabel("Assists Made in Game")
    plt.grid(visible=True, alpha=0.5)

    for stats in data.values():
        bx.scatter(stats["BLK"], stats["A"], color="green")


def main():
    cleaned_for_goals = remove_keys(cleaned_data.copy(), ["G"], keep=True)
    cleaned_for_plot = remove_keys(cleaned_data.copy(), ["A", "BLK"], keep=True)

    plt.figure(1)
    plot_first(cleaned_for_goals)

    plt.figure(2)
    plot_second(cleaned_for_plot)
    plt.show()

    exit(0)


if __name__ == '__main__':
    main()
