#!/usr/bin/python3

import sys
from binomial.arguments_reader import *
from binomial.print import *

config = read_arguments(
	"Finds single trial success probability that is needed to achieve the given amount of successes with the given amount of trials, and probability of success on each trial",
	["max_successes", "target_trials_or_time", "target_probability", "trials_per_time_unit"],
	{"max_successes": "int_value", "target_trials_or_time": "int_value", "target_probability": "float_value"}
)
if config == None:
	exit()


trials = config.target_trials
successes = config.max_successes
check = CheckType.AT_LEAST
check_chance = config.target_probability
max_error = 0.00001


print_found_probability(check, trials, successes, check_chance, max_error)
