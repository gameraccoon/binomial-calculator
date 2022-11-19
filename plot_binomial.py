#!/usr/bin/python3

from array import array
from binomial.calculate import *
import plotly.express as px
import sys

# default parameters
trials = 150
max_successes = 4
single_trial_success_chance = 0.08
cap_at_max = True
graph_type = "line" # "line" or "area"

# read parameters
if len(sys.argv) > 3:
	trials = int(sys.argv[1])
	max_successes = int(sys.argv[2])
	single_trial_success_chance = float(sys.argv[3])
	if len(sys.argv) > 4:
		graph_type = sys.argv[4]

raw_data = []

# init empty arrays
for line_idx in range(0, max_successes + 1):
	raw_data.append(array('f'))

# fill arrays with probabilities of each success on each step
last_iteration_idx = max_successes - 1 if cap_at_max else max_successes
for line_idx in range(0, last_iteration_idx + 1):
	for step_idx in range(0, line_idx):
		raw_data[line_idx].append(0.0)
	for step_idx in range(line_idx, trials + 1):
		raw_data[line_idx].append(get_binomial_probability(single_trial_success_chance, step_idx, line_idx))

# if needed, set last success values with cumulative values for "at least" instead of "exactly"
if cap_at_max:
	for step_idx in range(0, max_successes):
		raw_data[max_successes].append(0.0)
	for step_idx in range(max_successes, trials + 1):
		raw_data[max_successes].append(1.0 - get_cumulative_minus_binomial_probability(single_trial_success_chance, step_idx, max_successes))

# convert data to something that plotly can draw
data = {}
data["base"] = raw_data[0]
labels = ["base"]
for line_idx in range(1, max_successes + 1):
	if line_idx == max_successes and cap_at_max:
		step_name = "final step"
	else:
		step_name = "step{}".format(line_idx)

	data[step_name] = raw_data[line_idx]
	labels.append(step_name)

# draw
labels = {"index":"trial", "value":"probability"}
title = "Probability to have specific number of successes per trials, with single trial success probability of {}".format(single_trial_success_chance)
if graph_type == "line":
	fig = px.line(data, labels=labels, title=title)
elif graph_type == "area":
	fig = px.area(data, labels=labels, title=title)
else:
	sys.exit("Unknown graph type, use 'line' or 'area'")

fig.show()
