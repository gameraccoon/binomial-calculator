#!/usr/bin/python3

import sys
import random
from binomial.arguments_reader import *
from binomial.calculate import *

config = read_arguments(
	"Finds single trial success probability that is needed to achieve the given amount of successes on average with the given amount of trials",
	["max_successes", "target_trials_or_time", "trials_per_time_unit"],
	{"max_successes": "int_value", "target_trials_or_time": "int_value"}
)
if config == None:
	exit()

successes = config.max_successes
target_trials = config.target_trials

single_success_probability = find_single_trial_probability_by_average_trials(successes, target_trials)

print("{} trials are needed on average to achieve {} successes if a single trial success probability is {}".format(successes, target_trials, single_success_probability))
