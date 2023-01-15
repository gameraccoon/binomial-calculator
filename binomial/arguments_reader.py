#!/usr/bin/python3

import os
import sys
import textwrap
from binomial.config import *


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
	terminal_width = os.get_terminal_size().columns
	arg_map = build_arg_map()
	if "help" in arg_map:
		script_name = os.path.splitext(sys.argv[0])[0]

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
		return read_config(arg_map["config"])

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
		if not arg in arguments_map:
			print("Unknown option '{}', use --help to see the list of available options".format(arg))
			is_correct = False
	for mandatory_arg in mandatory_arguments:
		if not mandatory_arg in arg_map:
			print("Missing mandatory argument '--{}' refer to --help for more details".format(mandatory_arg))
			is_correct = False


	if not is_correct:
		return None

	return read_from_data(arg_map)
