#!/usr/bin/python3

import sys
from binomial.arguments_reader import *
from binomial.print import *

config = read_arguments(
	"Print cumulative chances of getting the provided amount of successes after doing the given amount of trials with the given success of a single trial ",
	["single_success_probability", "max_successes", "max_trials_or_time"],
	{"single_success_probability": "float_value", "max_successes": "int_value", "max_trials_or_time" : "int_value"}
)
if config == None:
	exit()

trials = config.max_trials
successes = config.max_successes
single_success_probability = config.single_success_probability
print(trials, successes, single_success_probability)


print_probabilities(single_success_probability, trials, successes)
