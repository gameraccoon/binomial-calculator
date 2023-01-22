#!/usr/bin/python3

import os
import sys
import textwrap
from binomial.config import *

extra_arguments = ["help", "config"]

def build_arg_map():
	arg_map = {}
	key = ""
	for arg in sys.argv[1:]:
		if arg.startswith("--"):
			if key != "":
				arg_map[key] = True
			key = arg[2:]
		else:
			if key != "":
				arg_map[key] = arg
				key = ""
			else:
				print("Unexpected option '{}', did you forget to add '--'?".format(arg))

	if key != "":
		arg_map[key] = True

	return arg_map


def get_argument_names(argument, argument_data):
	names = "--" + argument
	if argument_data.short_code != "":
		names += " --" + argument_data.short_code
	return names


def read_arguments(help, meaningful_arguments, mandatory_arguments):
	config: Config = None

	# validate requirements
	for arg in mandatory_arguments:
		if arg not in meaningful_arguments:
			print("Argument '{}' marked as mandatory but it is not in the list of meaningful arguments".format(arg))
			exit(1)
		if arg not in arguments_map:
			print("Argument '{}' is not part of config.py".format(arg))
			exit(1)

	terminal_width = os.get_terminal_size().columns
	script_name = os.path.splitext(sys.argv[0])[0]
	arg_map = build_arg_map()
	if "help" in arg_map:
		print(textwrap.fill(help, terminal_width))
		print("\nUsage:")
		print("  {} --config <path>".format(script_name))
		usage_example = "  {}".format(script_name)
		for arg in mandatory_arguments:
			short_code = arguments_map[arg].short_code
			usage_example += " --{}".format(short_code if short_code != "" else arg)
			v = mandatory_arguments[arg]
			if v != "":
				usage_example += " <{}>".format(v)
		print(usage_example)
		print("\nOptions:")
		longest_name = 0
		for argument in meaningful_arguments:
			longest_name = max(longest_name, len(get_argument_names(argument, arguments_map[argument])))

		for argument in meaningful_arguments:
			argument_data = arguments_map[argument]
			names = get_argument_names(argument, argument_data)
			argument_description = "  {}{}".format(names, " "*(2+longest_name-len(names)))
			chunk_size = terminal_width - longest_name - 4
			description_lines = textwrap.fill(argument_data.description, chunk_size).split("\n")
			argument_description += description_lines[0]
			for line in description_lines[1:]:
				argument_description += "\n" + " "*(4+longest_name) + line
			print(argument_description)
		return None
	elif "config" in arg_map:
		config = read_config(arg_map["config"])

	# replace short codes with full ones
	while True:
		for arg in arg_map:
			if arg in short_arguments_map:
				arg_map[short_arguments_map[arg]] = arg_map[arg]
				del arg_map[arg]
				break
		else:
			break

	# validate arguments
	is_correct = True
	for arg in arg_map:
		if not arg in arguments_map and (config == None or not arg in extra_arguments):
			print("Unknown option '{}'".format(arg))
			is_correct = False
		elif not arg in meaningful_arguments and (config == None or not arg in extra_arguments):
			print("Option '{}' doesn't make sense in context of this script".format(arg))
			is_correct = False
	if is_correct and config == None:
		for mandatory_arg in mandatory_arguments:
			if not mandatory_arg in arg_map:
				print("Missing mandatory option '--{}'".format(mandatory_arg))
				is_correct = False


	if not is_correct:
		print("See '{} --help' for more info".format(script_name))
		return None

	return read_from_data(config, arg_map)
