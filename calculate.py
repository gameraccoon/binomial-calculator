#!/usr/bin/python

from enum import Enum
import math
import sys


def get_binomial_probability(single_trial_success_chance, trials_count, number_of_successes):
	number_of_combinations = math.factorial(trials_count)/(math.factorial(number_of_successes) * math.factorial(trials_count - number_of_successes))
	return number_of_combinations * math.pow(single_trial_success_chance, number_of_successes) * math.pow(1.0 - single_trial_success_chance, trials_count - number_of_successes)


def get_cumulative_and_binomial_probabilities(single_trial_success_chance, trials_count, number_of_successes):
	binomial_probability = get_binomial_probability(single_trial_success_chance, trials_count, number_of_successes)

	cumulative_probability = binomial_probability
	for i in range(0, number_of_successes):
		cumulative_probability += get_binomial_probability(single_trial_success_chance, trials_count, i)

	return cumulative_probability, binomial_probability


def get_cumulative_probability(single_trial_success_chance, trials_count, number_of_successes):
	cumulative_probability, _ = get_cumulative_and_binomial_probabilities(single_trial_success_chance, trials_count, number_of_successes)
	return cumulative_probability


def get_cumulative_minus_binomial_probability(single_trial_success_chance, trials_count, number_of_successes):
	cumulative_probability, binomial_probability = get_cumulative_and_binomial_probabilities(single_trial_success_chance, trials_count, number_of_successes)
	return cumulative_probability - binomial_probability


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


def find_probability(function, target_probability, max_error, sign):
	single_trial_probability = 0.5
	result = function(single_trial_probability)
	error = math.fabs(target_probability - result)
	step = 0.25
	while error > max_error:
		if step == 0:
			sys.exit("We got into infinite loop, we probably can't reach this probability with these parameters")

		single_trial_probability += (step if (target_probability < result) else -step) * sign
		error = math.fabs(target_probability - result)
		step *= 0.5
		result = function(single_trial_probability)

	return single_trial_probability


CheckType = Enum('CheckType', ['EXACTLY', 'AT_LEAST', 'AT_MOST', 'LESS_THAN', 'MORE_THAN'])


def print_found_probability(check_type, trials_count, number_of_successes, target_probability, max_error):
	if number_of_successes > trials_count:
		sys.exit("Number of successes ({succ}) can't be greater than trial counts ({trial})".format(succ = number_of_successes, trial = trials_count))
	if target_probability < 0.0 or target_probability > 1.0:
		sys.exit("Target probability should be in range [0.0, 1.0], current value is {}".format(target_probability))

	if check_type == CheckType.EXACTLY:
		binomial_function = lambda a : get_binomial_probability(a, trials_count, number_of_successes)
		relation_text = "exactly"
		sign = 1
	elif check_type == CheckType.LESS_THAN:
		binomial_function = lambda a : get_cumulative_minus_binomial_probability(a, trials_count, number_of_successes)
		relation_text = "less than"
		sign = 1
	elif check_type == CheckType.AT_MOST:
		binomial_function = lambda a : get_cumulative_probability(a, trials_count, number_of_successes)
		relation_text = "at most"
		sign = 1
	elif check_type == CheckType.MORE_THAN:
		binomial_function = lambda a : (1.0 - get_cumulative_probability(a, trials_count, number_of_successes))
		relation_text = "more than"
		sign = -1
	elif check_type == CheckType.AT_LEAST:
		binomial_function = lambda a : (1.0 - get_cumulative_minus_binomial_probability(a, trials_count, number_of_successes))
		relation_text = "at least"
		sign = -1
	else:
		sys.exit("Unknown type of searching probability: {}".format(check_type))

	text = "To have {target} chance of {relation} {successes} successes in {trials} trials we need each trial to have probability to succeed of {result}\n"

	found_probability = find_probability(binomial_function, target_probability, max_error, sign)

	print(text.format(target = target_probability, relation = relation_text, successes = number_of_successes, trials = trials_count, result = found_probability))
	print_probabilities(found_probability, trials_count, number_of_successes)


trials = 2
successes = 1
check = CheckType.AT_LEAST
check_chance = 0.75
max_error = 0.00001

if len(sys.argv) > 3:
	trials = int(sys.argv[1])
	successes = int(sys.argv[2])
	check_chance = float(sys.argv[3])


print_found_probability(check, trials, successes, check_chance, max_error)
