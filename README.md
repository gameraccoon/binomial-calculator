A small set of functions to calculate, plot and compare probabilities

### Find a probability of a chest containing a piece of map, so that on average a player needs to spend 10 minutes to find at least 9 pieces of map if the player opens 2 new chests per minute

```
python find_single_trial_probability_by_average_trials_to_success.py --max_successes 9 --target_trials_or_time 10 --trials_per_time_unit 2.0 --time_units minutes
```

or

```
python find_single_trial_probability_by_average_trials_to_success.py --ms 7 --tt 10 --tptu 2 --tu minutes
```

result

```
10 minutes are needed on average to achieve 9 successes if a single trial success probability is 0.45
```

### With probability of 0.45 of finding a map in a chest and player opening 2 new chests per minute, find how much time is needed to at least 5, 25, 50, 75 and 95 percent of players to find at least 9 pieces of map

```
python print_characteristics.py --single_success_probability 0.45 --max_successes 9 --time_units minutes --trials_per_time_unit 2.0 --percentiles 5,25,50,75,95
```

or

```
python print_characteristics.py --ssp 0.45 --ms 9 --tu minutes --tptu 2.0 --pc 5,25,50,75,95
```

result

```
On average 10 minutes are needed to reach 9 successes with single trial success probability of 0.45
In about 5% of cases, 9 successes will be acheived in 6 minutes or less
In about 25% of cases, 9 successes will be acheived in 8 minutes or less
In about half of cases 9 successes will be acheived in 9.5 minutes or more
In about 25% of cases, 9 successes will be acheived in 11 minutes or more
In about 5% of cases, 9 successes will be acheived in 14.5 minutes or more
```

### Print a graph visualizing groups of players found at least specific amount of maps in chests, if a player opens 2 new chests on average and probability of finding a map in a chest is 0.45

```
python plot_binomial.py --single_success_probability 0.45 --max_successes 9 --cap_at_max --trials_per_time_unit 2.0 --time_units minutes  --max_trials_or_time 20 --graph_type area
```

or

```
python plot_binomial.py --ssp 0.45 --ms 9 --cap --tptu 2.0 --tu minutes --mt 20 --gt area
```

result

![Screenshot from 2023-01-15 17-32-08](https://user-images.githubusercontent.com/24990031/212554140-d02c7dd1-7225-4109-b7bf-bc3150609480.png)

### Print graph of chances to get 9th map per opening a new chest, distributed by minutes, if a player opens 2 new chests per minute and probability to find map in a chest is 0.45

```
python plot_trials_to_success.py --max_trials_or_time 20 --max_successes 9 --single_success_probability 0.45 --trials_per_time_unit 2.0 --time_units minutes --percentiles 5,25,50,75,95
```

or

```
python plot_trials_to_success.py --mt 20 --ms 9 --ssp 0.45 --tptu 2.0 --tu minutes --pc 5,25,50,75,95
```

result

![Screenshot from 2023-01-15 17-54-30](https://user-images.githubusercontent.com/24990031/212554792-723680d3-3cfb-48bb-8330-336f60cfa4fc.png)

### Notes

Each command can be called with `--help` to see info about specific options.

There is also a possibility to put options into a json file not to repeat them and pass a config using option `--config config.json`.

To plot graphs, you need `plotly` to be instealled: `pip install plotly`
