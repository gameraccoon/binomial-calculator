#!/usr/bin/python3

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
	# skip the last step
	cumulative_probability = 0.0
	for i in range(0, number_of_successes):
		cumulative_probability += get_binomial_probability(single_trial_success_chance, trials_count, i)
	return cumulative_probability


def find_probability_with_function(function, target_probability, max_error, sign):
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


def find_probability(check_type, trials_count, number_of_successes, target_probability, max_error):
	if check_type == CheckType.EXACTLY:
		binomial_function = lambda a : get_binomial_probability(a, trials_count, number_of_successes)
		sign = 1
	elif check_type == CheckType.LESS_THAN:
		binomial_function = lambda a : get_cumulative_minus_binomial_probability(a, trials_count, number_of_successes)
		sign = 1
	elif check_type == CheckType.AT_MOST:
		binomial_function = lambda a : get_cumulative_probability(a, trials_count, number_of_successes)
		sign = 1
	elif check_type == CheckType.MORE_THAN:
		binomial_function = lambda a : (1.0 - get_cumulative_probability(a, trials_count, number_of_successes))
		sign = -1
	elif check_type == CheckType.AT_LEAST:
		binomial_function = lambda a : (1.0 - get_cumulative_minus_binomial_probability(a, trials_count, number_of_successes))
		sign = -1
	else:
		sys.exit("Unknown type of searching probability: {}".format(check_type))

	return find_probability_with_function(binomial_function, target_probability, max_error, sign)


def find_average(single_trial_success_chance, target_successes, max_error = 0.0):
	last_prob = 0.0
	prob = 0.0
	result = 0.0
	index = target_successes
	while prob < 1.0 - max_error:
		last_prob = prob
		prob = 1.0 - get_cumulative_minus_binomial_probability(single_trial_success_chance, index, target_successes)
		result += (prob - last_prob) * index
		index += 1
	return result


def find_single_trial_probability_by_average_trials(target_successes, target_average_trials_count, max_error):
	search_function = lambda a : find_average(a, target_successes, max_error)
	return find_probability_with_function(search_function, target_average_trials_count, 1.0, 1.0)
