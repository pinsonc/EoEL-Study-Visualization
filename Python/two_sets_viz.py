import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import statistics
import time
from datetime import datetime

data_path_1 = 'C:/git/EoEL-Study-Visualization/Data/20181127_v1_node9_Master_sanitized.LOG'
data_path_2 = 'C:/git/EoEL-Study-Visualization/Data/12.17.18/121718_DATA_07.LOG'
num_channels = 30
avg_span_1 = 1
avg_span_2 = 10
# Headers:
## Time, NR, Node ID, Channel (there are 30), Measurement

timestamp = []
measurement = []

timestamp_2 = []
measurement_2 = []

duration_measurement = 4 * 3600 * 30
epoch_start = 1544883908 #this needs to be hard coded from checking the data
epoch_end   = epoch_start + duration_measurement

# get one list of timestamps and one list of measurements
with open(data_path_1) as f:
    line_count = 0
    for line in f:
        if line[0] != '#':
            line_list = line.split('\t')
            timestamp.append(line_list[0])
            measurement.append(line_list[4].rstrip('\n'))

with open(data_path_2) as f:
    line_count = 0
    for line in f:
        if line[0] != '#':
            line_list = line.split('\t')
            timestamp_2.append(line_list[0])
            measurement_2.append(line_list[4].rstrip('\n'))

# Now I want to take the average or something percentile of the 30 measurements taken in a single second
num_measurements = int(len(measurement) / num_channels)
ranges_avg = np.zeros(shape=(num_measurements,3))

num_measurements_2 = int(len(measurement_2) / num_channels)
ranges_avg_2 = np.zeros(shape=(num_measurements_2,3))

# takes the percentile-th measurement of the num_channels channels taken in one second and adds them
# to a new list, averaged_measurements
percentile = 50
averaged_measurements = []
am_timestamps = []

averaged_measurements_2 = []
am_timestamps_2 = []

for i in range(1,num_measurements):
    cur_measure_range = measurement[((i-1)*num_channels):(i*num_channels)]
    cur_measure_range = np.asarray(cur_measure_range, dtype='float64') # convert to float for percentile function

    averaged_measurements.append(np.percentile(cur_measure_range, percentile)) # adds the 50th percentile (median)

    am_timestamps.append(i)

for i in range(1,num_measurements):
    # Calculate median filter with filter width (1 + 2*avg_span_1)
    ranges_avg[i,1] = statistics.median(averaged_measurements[max(0, i-avg_span_1):min(num_measurements,i+avg_span_1)])
    # Calculate median filter with filter width (1 + 2*avg_span_2)
    ranges_avg[i,2] = statistics.median(averaged_measurements[max(0, i-avg_span_2):min(num_measurements,i+avg_span_2)])

ranges_avg_inch = np.true_divide((ranges_avg[:,2]),25.4)
ranges_avg_feet = np.true_divide(ranges_avg_inch,12)
am_timestamps.append(0)

for i in range(1,num_measurements_2):
    cur_measure_range_2 = measurement_2[((i-1)*num_channels):(i*num_channels)]
    cur_measure_range_2 = np.asarray(cur_measure_range_2, dtype='float64') # convert to float for percentile function

    averaged_measurements_2.append(np.percentile(cur_measure_range_2, percentile)) # adds the 50th percentile (median)

    am_timestamps_2.append(i)

for i in range(1,num_measurements_2):
    # Calculate median filter with filter width (1 + 2*avg_span_1)
    ranges_avg_2[i,1] = statistics.median(averaged_measurements_2[max(0, i-avg_span_1):min(num_measurements_2,i+avg_span_1)])
    # Calculate median filter with filter width (1 + 2*avg_span_2)
    ranges_avg_2[i,2] = statistics.median(averaged_measurements_2[max(0, i-avg_span_2):min(num_measurements_2,i+avg_span_2)])

ranges_avg_inch_2 = np.true_divide((ranges_avg_2[:,2]),25.4)
ranges_avg_feet_2 = np.true_divide(ranges_avg_inch_2,12)
am_timestamps_2.append(0)

print(len(averaged_measurements))
print(len(am_timestamps))
print(len(ranges_avg_2))
print(len(am_timestamps_2))

cleaned_avg_feet = []
time_sim = []

# trim the data sets down to the shortest one
max_len = 0
if (len(ranges_avg_feet) > len(ranges_avg_feet_2)):
    max_len=len(ranges_avg_feet_2)
else:
    max_len=len(ranges_avg_feet)

for i in range(0, 3600 * 4):
    if ranges_avg_feet[i] < 20:
        time_sim.append(i)
        cleaned_avg_feet.append(ranges_avg_feet[i])

cleaned_avg_feet_2 = []
time_sim_2 = []

for i in range(0, 3600 * 4):
    if ranges_avg_feet_2[i] < 20:
        time_sim_2.append(i)
        cleaned_avg_feet_2.append(ranges_avg_feet_2[i])

plt.ylim(0,20)
plt.plot(time_sim,cleaned_avg_feet)
plt.plot(time_sim_2,cleaned_avg_feet_2)
# plt.axes([0,0,len(time_sim),20])
plt.title("Distance between two nodes over time")
plt.xlabel("Time")
plt.ylabel("Measurement (ft)")
plt.grid(True)
plt.show()
# "C:/git/EoEL-Study-Visualization/Plots/1217.png",
