#!/usr/bin/python3

from array import array
from binomial.arguments_reader import *
from binomial.calculate import *
import sys
import time

config = read_arguments(
	"Plots graphs of probabilities to get to specific number of successes as function of trials/time",
	["max_trials_or_time", "max_successes", "cap_at_max", "single_success_probability", "graph_type", "time_units", "trials_per_time_unit", "reference_config"],
	{"max_trials_or_time": "int_value", "max_successes": "int_value", "single_success_probability" : "float_value"}
)
if config == None:
	exit()

reference_config: Config = None
if config.reference_config_path != "":
	reference_config = read_config(config.reference_config_path)
	if reference_config == None:
		print("Reference confing with path '{}' can't be opened".format(config.reference_config_path))
		exit()
	if (config.trials_per_time_unit == 0.0) != (reference_config.trials_per_time_unit == 0.0):
		print("Both reference config and normal config should be measured with same time unit" + str(config.trials_per_time_unit) + " " + str(reference_config.trials_per_time_unit))
		exit()
	elif config.trials_per_time_unit != 0.0 and (config.time_units != reference_config.time_units):
		print("Both reference config and normal config should be measured with same time unit (found '{}' and '{}')".format(config.time_units, reference_config.time_units))
		exit()

# default parameters
graph_type = config.graph_type
measure_in_time = config.trials_per_time_unit != 0.0

print("import plotly")
import plotly.express as px
import plotly.graph_objects as go

print("calculate plot data")

# check how long time it took to calculate the data
time_start = time.time()


def calculate_raw_plot_data(cfg):
	result = []

	# init empty arrays
	for line_idx in range(0, cfg.max_successes + 1):
		result.append(array('f'))

	# fill arrays with probabilities of each success on each step
	last_iteration_idx = cfg.max_successes - 1 if cfg.cap_at_max else cfg.max_successes
	for line_idx in range(0, last_iteration_idx + 1):
		print("calculating success #{}".format(line_idx))
		for step_idx in range(0, line_idx):
			result[line_idx].append(0.0)
		for step_idx in range(line_idx, cfg.max_trials + 1):
			result[line_idx].append(get_binomial_probability(cfg.single_success_probability, step_idx, line_idx))

	# if needed, set last success values with cumulative values for "at least" instead of "exactly"
	if cfg.cap_at_max:
		print("calculating success #{}".format(cfg.max_successes))
		for step_idx in range(0, cfg.max_successes):
			result[cfg.max_successes].append(0.0)
		for step_idx in range(cfg.max_successes, cfg.max_trials + 1):
			result[cfg.max_successes].append(1.0 - get_cumulative_minus_binomial_probability(cfg.single_success_probability, step_idx, cfg.max_successes))

	return result


raw_data = calculate_raw_plot_data(config)
raw_reference_data = None
if reference_config:
	raw_reference_data = calculate_raw_plot_data(reference_config)


print("Time spent on calculating data:", time.time() - time_start)

print("prepare plot data")

# convert data to something that plotly can draw
def generate_plolty_data(cfg, raw, suffix = ""):
	plotly_data = {}
	plotly_data["no successes" + suffix] = raw[0]
	plots = ["no successes" + suffix]
	for line_idx in range(1, cfg.max_successes + 1):
		if line_idx == cfg.max_successes and cfg.cap_at_max:
			step_name = "{} or more".format(cfg.max_successes)
		elif line_idx == 1:
			step_name = "1 success"
		else:
			step_name = "{} successes".format(line_idx)

		plotly_data[step_name + suffix] = raw[line_idx]
		plots.append(step_name + suffix)

	plotly_data["time"] = []
	for line_idx in range(0, cfg.max_trials + 1):
		plotly_data["time"].append(line_idx / cfg.trials_per_time_unit if measure_in_time else line_idx)
	return plotly_data, plots

data, plots = generate_plolty_data(config, raw_data)
if reference_config:
	reference_data, reference_plots = generate_plolty_data(reference_config, raw_reference_data, " ref")

print("draw plot")

# draw
labels = {"index":"trial", "value":"probability", "time":(config.time_units if measure_in_time else "trials")}
title = "Probability to have specific number of successes per trials (single trial success probability is {})".format(config.single_success_probability)
if graph_type == "line":
	fig1 = px.line(data, x="time", y=plots, labels=labels, title=title)
elif graph_type == "area":
	fig1 = px.area(data, x="time", y=plots, labels=labels, title=title)
else:
	sys.exit("Unknown graph type, use 'line' or 'area'")

if reference_config == None:
	fig1.show()
else:
	if graph_type == "line":
		fig2 = px.line(reference_data, x="time", y=reference_plots, labels=labels, title=title)
	elif graph_type == "area":
		fig2 = px.area(reference_data, x="time", y=reference_plots, labels=labels, title=title)
	fig = go.Figure(data=fig1.data + fig2.data)
	fig.show()
