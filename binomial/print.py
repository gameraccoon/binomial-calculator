#!/usr/bin/python3

import sys
from binomial.calculate import *

def print_probabilities(single_trial_success_chance, trials_count, number_of_successes):
	if number_of_successes > trials_count:
		sys.exit("Number of successes ({succ}) can't be greater than trial counts ({trial})".format(succ = number_of_successes, trial = trials_count))
	if single_trial_success_chance < 0.0 or single_trial_success_chance > 1.0:
		sys.exit("Single success chance should be in range [0.0, 1.0], current value is {}".format(single_trial_success_chance))

	cumulative_probability, binomial_probability = get_cumulative_and_binomial_probabilities(single_trial_success_chance, trials_count, number_of_successes)

	print("One trial success probability is {}".format(single_trial_success_chance))
	print("Doing {} trials".format(trials_count))
	print("Chance of getting exactly {} successes is {}".format(number_of_successes, binomial_probability))
	print("Chance of getting less than {} successes is {}".format(number_of_successes, cumulative_probability - binomial_probability))
	print("Chance of getting at most {} successes is {}".format(number_of_successes, cumulative_probability))
	print("Chance of getting more than {} successes is {}".format(number_of_successes, 1.0 - cumulative_probability))
	print("Chance of getting at least {} successes is {}".format(number_of_successes, 1.0 - (cumulative_probability - binomial_probability)))


def print_found_probability(check_type, trials_count, number_of_successes, target_probability, max_error):
	if number_of_successes > trials_count:
		sys.exit("Number of successes ({succ}) can't be greater than trial counts ({trial})".format(succ = number_of_successes, trial = trials_count))
	if target_probability < 0.0 or target_probability > 1.0:
		sys.exit("Target probability should be in range [0.0, 1.0], current value is {}".format(target_probability))

	if check_type == CheckType.EXACTLY:
		relation_text = "exactly"
	elif check_type == CheckType.LESS_THAN:
		relation_text = "less than"
	elif check_type == CheckType.AT_MOST:
		relation_text = "at most"
	elif check_type == CheckType.MORE_THAN:
		relation_text = "more than"
	elif check_type == CheckType.AT_LEAST:
		relation_text = "at least"
	else:
		sys.exit("Unknown type of searching probability: {}".format(check_type))

	text = "To have {target} chance of {relation} {successes} successes in {trials} trials we need each trial to have probability to succeed of {result}\n"

	found_probability = find_probability(check_type, trials_count, number_of_successes, target_probability, max_error)

	print(text.format(target = target_probability, relation = relation_text, successes = number_of_successes, trials = trials_count, result = found_probability))
	print_probabilities(found_probability, trials_count, number_of_successes)

