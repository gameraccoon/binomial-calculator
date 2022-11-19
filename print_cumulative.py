#!/usr/bin/python3

import sys
from binomial.print import *


trials = 15
successes = 4
single_trial_success_chance = 0.5

if len(sys.argv) > 3:
	trials = int(sys.argv[1])
	successes = int(sys.argv[2])
	single_trial_success_chance = float(sys.argv[3])


print_probabilities(single_trial_success_chance, trials, successes)
