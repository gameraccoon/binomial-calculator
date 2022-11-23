#!/usr/bin/python3

from dataclasses import dataclass
import json
import math

@dataclass
class Config:
    single_trial_success_probability: float = 0.5
    max_successes: int = 2
    cap_at_max: bool = False
    measure_in_time: bool = False
    time_units: str = "sec"
    trials_per_time_unit: float = 1.0
    max_trials: int = 200
    target_trials: int = 140
    graph_type: str = "line" # "line" or "area"
    percentiles = []


def read_config(path):
    result = Config()

    with open(path, 'r') as f:
        data = json.load(f)
        result.cap_at_max = bool(data["cap_at_max"])
        result.single_trial_success_probability = float(data["single_trial_success_probability"])
        result.max_successes = int(data["max_successes"])
        result.measure_in_time = bool(data["measure_in_time"])
        result.time_units = data["time_units"]
        result.trials_per_time_unit = float(data["trials_per_time_unit"])
        result.max_trials = int(data["max_trials_or_time"])
        result.target_trials = int(data["target_trials_or_time"])
        result.graph_type = data["graph_type"]
        result.percentiles = data["percentiles"]

        if result.measure_in_time:
            result.max_trials = int(round(result.max_trials * result.trials_per_time_unit))
            result.target_trials = int(math.ceil(result.max_trials * result.trials_per_time_unit))

        for i in range(0, len(result.percentiles)):
            result.percentiles[i] = float(result.percentiles[i]) * 0.01

    return result