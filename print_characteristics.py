#!/usr/bin/python3

import sys
from binomial.print import *

target_successes = 4
single_trial_success_probability = 0.5

if len(sys.argv) > 2:
	target_successes = int(sys.argv[1])
	single_trial_success_probability = float(sys.argv[2])

percentile_1 = 0.05
percentile_3 = 0.95

percentile_1_value = -1
q1 = -1
median = -1
q3 = -1
percentile_3_value = -1

last_step_probability = 0.0
step_idx = target_successes
while percentile_3_value == -1 or q3 == -1:
	this_step_probability = 1.0 - get_cumulative_minus_binomial_probability(single_trial_success_probability, step_idx, target_successes)

	if last_step_probability < percentile_1 and this_step_probability > percentile_1:
		percentile_1_value = step_idx if this_step_probability - percentile_1 < percentile_1 - last_step_probability else step_idx - 1

	if last_step_probability < 0.25 and this_step_probability > 0.25:
		q1 = step_idx if this_step_probability - 0.25 < 0.25 - last_step_probability else step_idx - 1

	if last_step_probability < 0.5 and this_step_probability > 0.5:
		median = step_idx if this_step_probability - 0.5 < 0.5 - last_step_probability else step_idx - 1

	if last_step_probability < 0.75 and this_step_probability > 0.75:
		q3 = step_idx if this_step_probability - 0.75 < 0.75 - last_step_probability else step_idx - 1

	if last_step_probability < percentile_3 and this_step_probability > percentile_3:
		percentile_3_value = step_idx if this_step_probability - percentile_3 < percentile_3 - last_step_probability else step_idx - 1

	last_step_probability = this_step_probability
	step_idx += 1

avg = int(round(find_average(single_trial_success_probability, target_successes, 0.00001)))

print("In about {}% of cases, {} successes will be acheived in {} trials or less".format(int(percentile_1 * 100), target_successes, percentile_1_value))
print("In about 25% of cases, {} successes will be acheived in {} trials or less".format(target_successes, q1))
print("In about {} trials, half of the cases will have {} or more successes".format(median, target_successes))
print("On average {} trials is needed to reach {} successes".format(avg, target_successes))
print("In about 25% of cases, {} successes will be acheived in {} trials or more".format(target_successes, q3))
print("In about {}% of cases, {} successes will be acheived in {} trials or more".format(int((1.0 - percentile_3) * 100), target_successes, percentile_3_value))
