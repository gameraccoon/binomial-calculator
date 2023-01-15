#!/usr/bin/python3

import sys
from binomial.arguments_reader import *
from binomial.print import *

target_successes = 4
single_success_probability = 0.5

config = read_arguments(
	"Prints cumulative probabilities with the given probabilities of success on a single trial and amount of trials",
	["single_success_probability", "max_successes", "time_units", "trials_per_time_unit", "percentiles"],
	{"single_success_probability": "float_value", "max_successes": "int_value"}
)

if config == None:
	exit()

target_successes = config.max_successes
single_success_probability = config.single_success_probability


percentiles_count = len(config.percentiles)
percentile_values = [-1] * percentiles_count
next_percentile_to_update = 0
def update_percentile_values(prev_value, current_value, index):
	global next_percentile_to_update
	for i in range(next_percentile_to_update, percentiles_count):
		percentile = config.percentiles[i]
		if current_value > percentile:
			percentile_values[i] = index if current_value - percentile < percentile - prev_value else index - 1
			next_percentile_to_update = i + 1
		else:
			break
	else:
		next_percentile_to_update = percentiles_count


last_step_probability = 0.0
step_idx = target_successes
while next_percentile_to_update != percentiles_count:
	this_step_probability = 1.0 - get_cumulative_minus_binomial_probability(single_success_probability, step_idx, target_successes)

	update_percentile_values(last_step_probability, this_step_probability, step_idx)

	last_step_probability = this_step_probability
	step_idx += 1

avg = int(round(find_average(single_success_probability, target_successes)))

measure_in_time = config.trials_per_time_unit != 0.0
time_label = config.time_units if measure_in_time else "trials";
time_mult = 1.0 / config.trials_per_time_unit if measure_in_time else 1

def pretty_format_time(value):
	mult_value = value * time_mult
	if mult_value == int(mult_value):
		return int(mult_value)
	return round(mult_value, 2)

print("On average {} {} are needed to reach {} successes with single trial success probability of {}".format(pretty_format_time(avg), time_label, target_successes, single_success_probability))

for i in range(0, percentiles_count):
	percentile = config.percentiles[i]
	if percentile == 0.5:
		print("In about half of cases {} successes will be acheived in {} {} or more".format(target_successes, pretty_format_time(percentile_values[i]), time_label))
	elif percentile < 0.5:
		print("In about {}% of cases, {} successes will be acheived in {} {} or less".format(int(round(percentile * 100)), target_successes, pretty_format_time(percentile_values[i]), time_label))
	else:
		print("In about {}% of cases, {} successes will be acheived in {} {} or more".format(100 - int(round(percentile * 100)), target_successes, pretty_format_time(percentile_values[i]), time_label))
