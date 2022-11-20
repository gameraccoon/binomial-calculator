#!/usr/bin/python3

import sys
import random
from binomial.calculate import *

successes = 2
target_trials = 4
max_error = 0.00001

if len(sys.argv) > 2:
	successes = int(sys.argv[1])
	target_trials = int(sys.argv[2])
	if len(sys.argv) > 3:
		max_error = float(sys.argv[3])

single_trial_success_probability = find_single_trial_probability_by_average_trials(successes, target_trials, max_error)

print("With single trial success probability of {} we need on average {} trials to have {} successes".format(single_trial_success_probability, target_trials, successes))
