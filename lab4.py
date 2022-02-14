######################
# Nicholas Fiorito
# Lab 4
# 14 February 2022


# IMPORTS
import pandas as pd
import numpy as np


# GLOBALS
DELAYS = {"fire": {"chance": 0.01, "delay": 100},
          "derail": {"chance": 0.05, "delay": 30},
          "turkey": {"chance": .1, "delay": 2}}
EXPERIMENTS = 500
TRIALS = 1000


# FUNCTIONS
def simulate(num_simulations, num_reps, selection_values, selection_probabilities):
    # Define a list to keep all the results from each simulation that we want to analyze
    all_stats = []

    # Loop through many simulations
    for i in range(num_simulations):
        # Choose random inputs for the sales targets and percent to target
        ride_events = np.random.choice(selection_values, num_reps, replace=True, p=selection_probabilities)
        all_stats.append(ride_events)
    return all_stats


def calculate_delay(simulation_results):
    delay_sum = 0
    events = 0
    for ride in simulation_results:
        for event in ride:
            events += 1
            try:
                delay_sum += DELAYS[event]["delay"]
            except KeyError as e:
                pass
    return delay_sum / events


# TASKS
# MAIN
def main():
    # calculate the expected delay of a single train
    sim = simulate(1, 100, delay_types, delay_probabilities)
    sim_one_delay = calculate_delay(sim)
    print("the expected delay for a single train is %d minutes" % sim_one_delay)

    # determine independently whether or not this train has been affected and calculate the total cumulative delay
    sim_two_fire = simulate(1, 1, [delay_types[0], delay_types[3]], [DELAYS["fire"]["chance"], 0.99])
    sim_two_derail = simulate(1, 1, [delay_types[1], delay_types[3]], [DELAYS["derail"]["chance"], 0.95])
    sim_two_turkey = simulate(1, 1, [delay_types[2], delay_types[3]], [DELAYS["turkey"]["chance"], 0.9])

    sim_two_delay = 0
    for sim_two in sim_two_fire, sim_two_turkey, sim_two_derail:
        sim_two_delay += calculate_delay(sim_two)

    print("the expected delay independent delays on a single train is %d minutes" % sim_two_delay)

    # so many trains
    sim_three_fire = simulate(1, EXPERIMENTS, [delay_types[0], delay_types[3]], [DELAYS["fire"]["chance"], 0.99])
    sim_three_derail = simulate(1, EXPERIMENTS, [delay_types[1], delay_types[3]], [DELAYS["derail"]["chance"], 0.95])
    sim_three_turkey = simulate(1, EXPERIMENTS, [delay_types[2], delay_types[3]], [DELAYS["turkey"]["chance"], 0.9])

    sim_three_delay = 0
    for sim_three in sim_three_fire, sim_three_derail, sim_three_turkey:
        sim_three_delay += calculate_delay(sim_three)

    print("the mean amount of delay on a single train is %d minutes" % sim_three_delay)

    # so many trains
    sim_multi_fire = simulate(TRIALS, EXPERIMENTS, [delay_types[0], delay_types[3]], [DELAYS["fire"]["chance"], 0.99])
    sim_multi_derail = simulate(TRIALS, EXPERIMENTS, [delay_types[1], delay_types[3]], [DELAYS["derail"]["chance"], 0.95])
    sim_multi_turkey = simulate(TRIALS, EXPERIMENTS, [delay_types[2], delay_types[3]], [DELAYS["turkey"]["chance"], 0.9])

    sim_multi_delay = 0
    for sim_multi in sim_multi_fire, sim_multi_derail, sim_multi_turkey:
        sim_multi_delay += calculate_delay(sim_multi)

    print("the mean amount of delay over %d trials is %d minutes" % (TRIALS, sim_multi_delay))

if __name__ == '__main__':
    delay_types = []
    delay_probabilities = []
    delay_time = []
    delay_copy = DELAYS.copy()
    delay_copy["none"] = {"chance": 0.84, "delay": 0}

    for k, v in delay_copy.items():
        delay_types.append(k)
        delay_probabilities.append(v["chance"])
        delay_time.append(v["delay"])

    main()
    exit(0)
