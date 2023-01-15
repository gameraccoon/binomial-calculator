#!/usr/bin/python3

from dataclasses import dataclass
import json
import math

@dataclass
class Config:
    single_success_probability: float = 0.0
    max_successes: int = 0
    cap_at_max: bool = False
    time_units: str = "sec"
    trials_per_time_unit: float = 0.0
    max_trials: int = 0
    target_trials: int = 0
    target_probability: float = 0.0
    graph_type: str = "line" # "line" or "area"
    percentiles = []


@dataclass
class ArgumentData:
    short_code: str = ""
    description: str = ""


arguments_map = {
    "single_success_probability": ArgumentData("sp", "Success probability of a single trial"),
    "max_successes": ArgumentData("ms", "Amount of successes we're targeting to reach"),
    "cap_at_max": ArgumentData("cap", "Set if we can't reach more successes than max_successes"),
    "time_units": ArgumentData("tu", "Time unit to measure in, e.g. 'sec'"),
    "trials_per_time_unit": ArgumentData("tptu", "How many trials can happen per time unit e.g. '--tptu 0.5', time units will not be used if this value is not specified"),
    "max_trials_or_time": ArgumentData("mt", "Max trials or time we need to account for"),
    "target_trials_or_time": ArgumentData("tgt", "How many trials we're interested in"),
    "target_probability": ArgumentData("tp", "Target probability that we are aiming for"),
    "graph_type": ArgumentData("gt", "Graph type: 'line' or 'area'"),
    "percentiles": ArgumentData("pct", "Comma-separated list of percentiles (in percent) to calculate, e.g. '--pct 25,50,75'"),
}

short_arguments_map = {}
for arg in arguments_map:
    short_arg = arguments_map[arg].short_code
    if short_arg != "":
        short_arguments_map[short_arg] = arg


def read_from_data(data):
    result = Config()

    result.cap_at_max = bool(data.get("cap_at_max", Config.cap_at_max))
    result.single_success_probability = float(data.get("single_success_probability", Config.single_success_probability))
    result.max_successes = int(data.get("max_successes", Config.max_successes))
    result.time_units = data.get("time_units", Config.time_units)
    result.trials_per_time_unit = float(data.get("trials_per_time_unit", Config.trials_per_time_unit))
    result.max_trials = int(data.get("max_trials_or_time", Config.max_trials))
    result.target_trials = int(data.get("target_trials_or_time", Config.target_trials))
    result.target_probability = float(data.get("target_probability", Config.target_probability))
    result.graph_type = data.get("graph_type", Config.graph_type)
    result.percentiles = data.get("percentiles", Config.percentiles)

    if result.trials_per_time_unit != 0.0:
        result.max_trials = int(round(result.max_trials * result.trials_per_time_unit))
        result.target_trials = int(math.ceil(result.target_trials * result.trials_per_time_unit))

    if isinstance(result.percentiles, str):
        result.percentiles = result.percentiles.split(",")
    for i in range(0, len(result.percentiles)):
        result.percentiles[i] = float(result.percentiles[i]) * 0.01

    return result


def read_config(path):
    if not isinstance(path, str) or path == "":
        print("No config file provided")
        return None

    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return read_from_data(data)
    except:
        print("Can't open config file '{}'".format(path))
        return None
