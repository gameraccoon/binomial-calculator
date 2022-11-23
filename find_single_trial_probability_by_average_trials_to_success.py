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

print("To have {} successes {} trials are needed on average if single trial success probability is {}".format(successes, target_trials, single_trial_success_probability))
