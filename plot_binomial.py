#!/usr/bin/python3

print("import dependencies")

from array import array
from binomial.calculate import *
from binomial.config import *
import plotly.express as px
import sys
import time

print("read configs")

config_path = "config.json"

# read parameters
if len(sys.argv) > 1:
	config_path = sys.argv[1]

config = read_config(config_path)

# default parameters
trials = config.max_trials
max_successes = config.max_successes
single_trial_success_probability = config.single_trial_success_probability
cap_at_max = config.cap_at_max
graph_type = config.graph_type
measure_in_time = config.measure_in_time


print("calculate plot data")

raw_data = []
# check how long time it took to calculate the data
time_start = time.time()

# init empty arrays
for line_idx in range(0, max_successes + 1):
	raw_data.append(array('f'))

# fill arrays with probabilities of each success on each step
last_iteration_idx = max_successes - 1 if cap_at_max else max_successes
for line_idx in range(0, last_iteration_idx + 1):
	print("calculating success #{}".format(line_idx))
	for step_idx in range(0, line_idx):
		raw_data[line_idx].append(0.0)
	for step_idx in range(line_idx, trials + 1):
		raw_data[line_idx].append(get_binomial_probability(single_trial_success_probability, step_idx, line_idx))

# if needed, set last success values with cumulative values for "at least" instead of "exactly"
if cap_at_max:
	print("calculating success #{}".format(max_successes))
	for step_idx in range(0, max_successes):
		raw_data[max_successes].append(0.0)
	for step_idx in range(max_successes, trials + 1):
		raw_data[max_successes].append(1.0 - get_cumulative_minus_binomial_probability(single_trial_success_probability, step_idx, max_successes))

print("Time spent on calculating data:", time.time() - time_start)

print("prepare plot data")

# convert data to something that plotly can draw
data = {}
data["no successes"] = raw_data[0]
plots = ["no successes"]
for line_idx in range(1, max_successes + 1):
	if line_idx == max_successes and cap_at_max:
		step_name = "{} or more".format(max_successes)
	elif line_idx == 1:
		step_name = "1 success"
	else:
		step_name = "{} successes".format(line_idx)

	data[step_name] = raw_data[line_idx]
	plots.append(step_name)

data["time"] = []
for line_idx in range(0, trials + 1):
	data["time"].append(line_idx / config.trials_per_time_unit if measure_in_time else line_idx)

print("draw plot")

# draw
labels = {"index":"trial", "value":"probability", "time":(config.time_units if measure_in_time else "trials")}
title = "Probability to have specific number of successes per trials (single trial success probability is {})".format(single_trial_success_probability)
if graph_type == "line":
	fig = px.line(data, x="time", y=plots, labels=labels, title=title)
elif graph_type == "area":
	fig = px.area(data, x="time", y=plots, labels=labels, title=title)
else:
	sys.exit("Unknown graph type, use 'line' or 'area'")

fig.show()
