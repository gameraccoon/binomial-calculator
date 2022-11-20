#!/usr/bin/python3

print("import dependencies")

from array import array
from binomial.calculate import *
import plotly.express as px
import sys

# default parameters
trials = 150
max_successes = 4
single_trial_success_probability = 0.08
percentile_1 = 0.25
percentile_3 = 0.75

# read parameters
if len(sys.argv) > 3:
	trials = int(sys.argv[1])
	max_successes = int(sys.argv[2])
	single_trial_success_probability = float(sys.argv[3])

	if len(sys.argv) > 5:
		percentile_1 = float(sys.argv[4]) / 100.0
		percentile_3 = float(sys.argv[5]) / 100.0

raw_data = array('f')
percentile_1_value = -1
percentile_3_value = -1
median = -1

print("calculate plot data")

# fill each step with the value of probability contributing on that step
for step_idx in range(0, max_successes):
	raw_data.append(0.0)
last_step_probability = 0.0
for step_idx in range(max_successes, trials + 1):
	this_step_probability = 1.0 - get_cumulative_minus_binomial_probability(single_trial_success_probability, step_idx, max_successes)
	raw_data.append(this_step_probability - last_step_probability)

	if last_step_probability < percentile_1 and this_step_probability > percentile_1:
		percentile_1_value = step_idx if this_step_probability - percentile_1 < percentile_1 - last_step_probability else step_idx - 1

	if last_step_probability < 0.5 and this_step_probability > 0.5:
		median = step_idx if this_step_probability - 0.5 < 0.5 - last_step_probability else step_idx - 1

	if last_step_probability < percentile_3 and this_step_probability > percentile_3:
		percentile_3_value = step_idx if this_step_probability - percentile_3 < percentile_3 - last_step_probability else step_idx - 1

	last_step_probability = this_step_probability

print("calculate average")

avg = int(round(find_average(single_trial_success_probability, max_successes, 0.00001)))

print("prepare plot data")

# draw
labels = {"index":"trial", "value":"probability"}
title = "Probability to reach {} successes on a given trial (single trial success probability is {})".format(max_successes, single_trial_success_probability)

fig = px.line(raw_data.tolist(), labels=labels, title=title)

if percentile_1_value != -1:
	fig.add_annotation(x=percentile_1_value, y=raw_data[percentile_1_value], text="q1" if percentile_1 == 0.25 else "{}th percentile".format(int(100 * percentile_1)), hovertext="{} trials give approx {}% chance of reaching at least {} successes".format(percentile_1_value, int(percentile_1 * 100), max_successes))
if percentile_3_value != -1:
	fig.add_annotation(x=percentile_3_value, y=raw_data[percentile_3_value], text="q3" if percentile_3 == 0.75 else "{}th percentile".format(int(100 * percentile_3)), hovertext="{} trials give approx {}% chance of reaching at least {} successes".format(percentile_3_value, int(percentile_3 * 100), max_successes))
if median != -1:
	fig.add_annotation(x=median, y=raw_data[median], text="median", hovertext="{} trials give approx 50% chance of reaching at least {} successes".format(median, max_successes))
if avg < trials:
	fig.add_annotation(x=avg, y=raw_data[avg], text="avg", hovertext="Need on average {} trials to reach {} successes".format(avg, max_successes))

print("draw plot")

fig.show()
