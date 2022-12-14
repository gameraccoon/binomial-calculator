#!/usr/bin/python3

print("import dependencies")

from array import array
from binomial.calculate import *
from binomial.config import *
import plotly.express as px
import sys

print("read configs")

config_path = "config.json"

# read parameters
if len(sys.argv) > 1:
	config_path = sys.argv[1]

config = read_config(config_path)


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


# default parameters
trials = config.max_trials
max_successes = config.max_successes
single_trial_success_probability = config.single_trial_success_probability
measure_in_time = config.measure_in_time

print("calculate plot data")

raw_data = array('f')
# fill each step with the value of probability contributing on that step
for step_idx in range(0, max_successes):
	raw_data.append(0.0)
last_step_probability = 0.0
for step_idx in range(max_successes, trials + 1):
	this_step_probability = 1.0 - get_cumulative_minus_binomial_probability(single_trial_success_probability, step_idx, max_successes)
	raw_data.append(this_step_probability - last_step_probability)

	update_percentile_values(last_step_probability, this_step_probability, step_idx)

	last_step_probability = this_step_probability

print("calculate average")

avg = int(round(find_average(single_trial_success_probability, max_successes, 0.00001)))

print("prepare plot data")

x_label = config.time_units if measure_in_time else "trials";
x_mult = 1.0 / config.trials_per_time_unit if measure_in_time else 1
data = {"probabilities" : raw_data.tolist(), "time": []}
for line_idx in range(0, trials + 1):
	data["time"].append(line_idx * x_mult)

labels = {"index":"trial", "value":"probability", "time":x_label}
title = "Probability to reach {} successes on a given trial (single trial success probability is {})".format(max_successes, single_trial_success_probability)

fig = px.line(data, x="time", y="probabilities", labels=labels, title=title)

for i in range(0, percentiles_count):
	percentile = config.percentiles[i]
	x_value = percentile_values[i]*x_mult
	if x_value < 0.0:
		continue

	y_value = raw_data[percentile_values[i]]
	if percentile == 0.5:
		fig.add_annotation(x=x_value, y=y_value, text="median", hovertext="{} {} give approx 50% chance of reaching at least {} successes".format(x_value, x_label, max_successes))
	elif percentile == 0.25:
		fig.add_annotation(x=x_value, y=y_value, text="q1", hovertext="{} {} give approx 25% chance of reaching at least {} successes".format(x_value, x_label, max_successes))
	elif percentile == 0.75:
		fig.add_annotation(x=x_value, y=y_value, text="q3", hovertext="{} {} give approx 75% chance of reaching at least {} successes".format(x_value, x_label, max_successes))
	else:
		fig.add_annotation(x=x_value, y=y_value, text="{}th percentile".format(int(round(100 * percentile))), hovertext="{} {} give approx {}% chance of reaching at least {} successes".format(x_value, x_label, int(percentile * 100), max_successes))

if avg < trials:
	fig.add_annotation(x=avg*x_mult, y=raw_data[avg], text="avg", hovertext="Need on average {} {} to reach {} successes".format(avg*x_mult, x_label, max_successes))

print("draw plot")

fig.show()
