#!/usr/bin/python3

import sys
from binomial.print import *


trials = 15
successes = 4
check = CheckType.AT_LEAST
check_chance = 0.5
max_error = 0.00001

if len(sys.argv) > 3:
	trials = int(sys.argv[1])
	successes = int(sys.argv[2])
	check_chance = float(sys.argv[3])


print_found_probability(check, trials, successes, check_chance, max_error)
