import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics

data_path = 'C:/git/EoEL-Study-Visualization/Data/12.17.18/121718_DATA_07.LOG'
num_channels = 30
avg_span_1 = 1
avg_span_2 = 10
# Headers:
## Time, NR, Node ID, Channel (there are 30), Measurement

timestamp = []
measurement = []

# get one list of timestamps and one list of measurements
with open(data_path) as f:
    line_count = 0
    for line in f:
        if line[0] != '#':
            line_list = line.split('\t')
            timestamp.append(line_list[0])
            measurement.append(line_list[4].rstrip('\n'))

# Now I want to take the average or something percentile of the 30 measurements taken in a single second
num_measurements = int(len(measurement) / num_channels)
ranges_avg = np.zeros(shape=(num_measurements,3))

# takes the percentile-th measurement of the num_channels channels taken in one second and adds them
# to a new list, averaged_measurements
percentile = 50
averaged_measurements = []
am_timestamps = []
for i in range(1,num_measurements):
    cur_measure_range = measurement[((i-1)*num_channels):(i*num_channels)]
    cur_measure_range = np.asarray(cur_measure_range, dtype='float64') # convert to float for percentile function

    averaged_measurements.append(np.percentile(cur_measure_range, percentile)) # adds the 50th percentile (median)

    am_timestamps.append(timestamp[(i-1)*num_channels])

for i in range(1,num_measurements):
    # Calculate median filter with filter width (1 + 2*avg_span_1)
    ranges_avg[i,1] = statistics.median(averaged_measurements[max(0, i-avg_span_1):min(num_measurements,i+avg_span_1)])
    # Calculate median filter with filter width (1 + 2*avg_span_2)
    ranges_avg[i,2] = statistics.median(averaged_measurements[max(0, i-avg_span_2):min(num_measurements,i+avg_span_2)])

ranges_avg_inch = np.true_divide((ranges_avg[:,2]),25.4)
ranges_avg_feet = np.true_divide(ranges_avg_inch,12)

am_timestamps.append(0)

print(len(am_timestamps))
print(len(averaged_measurements))
plt.plot(am_timestamps,ranges_avg_feet)
plt.title("Distance between two nodes over time")
plt.xlabel("Time")
plt.ylabel("Measurement (ft)")
plt.grid(True)
plt.savefig("C:/git/EoEL-Study-Visualization/Plots/1217.png")
