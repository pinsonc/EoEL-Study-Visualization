# Ecology of Early Life Study Visualization

The original scripts are in the `MATLAB` folder. I did not push the data for privacy concerns once we start working with real data (as well as size concerns)

## Folder Breakdown
### MATLAB
These scripts were provided by the Berkeley lab. They served as the basis for the Python scripts we wrote.  


### Python
Each of the scripts in here are modifications of the `eval_mobility_vanderbilt.m` file found in the `MATLAB` folder. Each is used depending on what sort of plot you would like to generate.
#### `two_sets_viz.py` [verbose]
Used for displaying two sets of data on the same plot.

**Variables:**

* `data_path_1` is a `string` variable that represents the relative (or absolute) path to the raw output (a `.LOG` file) from the TotTag
* `data_path_2` is a `string` variable that represents the relative (or absolute) path to the raw output (a `.LOG` file) from the TotTag
#### `viz_multinode.py` [verbose]
Used for displaying data which has more than two nodes in the same network.

**Variables:**

* `path` is a `string` variable that represents the relative (or absolute) path to the raw output (a `.LOG` file) from the TotTag

This script is only of interest when one node is ranging to two different nodes at the same time.

#### `viz_simple_data.py` [simple]
Used for displaying a single file of the simplified data mode.

**Variables:**

* `filename` is a `string` that represents the name of the file you are trying to graph
* `data_path` is a `string` that represents the folder containing the file you are trying to graph

The reason I broke it up that way instead of using the same path method from above is that this can be easily adapted to iterate over all files in a folder and generate graphs for a batch of files instead of just one.
#### `viz.py` [verbose]
Used for displaying a single file of the verbose data mode.

**Variables:**

* `data_path` is a `string` variable that represents the relative (or absolute) path to the raw output (a `.LOG` file) from the TotTag

## Data modes [verbose vs. simple]
### Verbose:
```
2906389050	016133	10	00	0000000193
2906389050	016133	10	01	4294966868
2906389050	016133	10	02	0000000228
2906389050	016133	10	03	0000000279
2906389050	016133	10	04	4294967146
2906389050	016133	10	05	0000000458
```
The devices take 30 measurements each second. Each one is outputted here and displayed next to the timestamp with channel (or number of the measurement). To display this data we calculate a moving average to condense them all to one measurement per timestamp.
### Simple:
```
### HEADER for file 'data.log'; Date: 2019/10/10 13:17:53
1570713482	c0:98:e5:42:00:00:00:2d	000249
1570713483	c0:98:e5:42:00:00:00:2d	000474
1570713484	c0:98:e5:42:00:00:00:2d	000157
1570713485	c0:98:e5:42:00:00:00:2d	026260
1570713486	c0:98:e5:42:00:00:00:2d	000150
1570713487	c0:98:e5:42:00:00:00:2d	000194
```
This is the same data as the verbose but it lists the node ranged with and it also precalculates the average. So there is only one entry per timestamp. This is the mode we are **primarily** working with these days. Somone would have had to manually change it if it is different.