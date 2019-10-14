import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics
import time
from datetime import datetime

data_path = 'C:/Users/pinso/Downloads/Lab Test 1/test1010/DATA2B_20191010_Test1.LOG'
num_channels = 30
avg_span_1 = 1
avg_span_2 = 10
# Headers:
## Time, NR, Node ID, Channel (there are 30), Measurement

timestamp = []
measurement = []

duration_measurement = 4 * 3600 * 30
epoch_start = 1544883908 #this needs to be hard coded from checking the data
epoch_end   = epoch_start + duration_measurement

# get one list of timestamps and one list of measurements
with open(data_path) as f:
    line_count = 0
    for line in f:
        if line[0] != '#':
            line_list = line.split('\t')
            timestamp.append(line_list[0])
            measurement.append(line_list[2].rstrip('\n'))

# Now I want to take the average or something percentile of the 30 measurements taken in a single second
num_measurements = int(len(measurement) / num_channels)
print(len(measurement)/30)
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

    am_timestamps.append(i)

for i in range(1,num_measurements):
    # Calculate median filter with filter width (1 + 2*avg_span_1)
    ranges_avg[i,1] = statistics.median(averaged_measurements[max(0, i-avg_span_1):min(num_measurements,i+avg_span_1)])
    # Calculate median filter with filter width (1 + 2*avg_span_2)
    ranges_avg[i,2] = statistics.median(averaged_measurements[max(0, i-avg_span_2):min(num_measurements,i+avg_span_2)])

ranges_avg_inch = np.true_divide((ranges_avg[:,2]),25.4)
ranges_avg_feet = np.true_divide(ranges_avg_inch,12)
am_timestamps.append(0)

print(len(ranges_avg_feet))

cleaned_avg_feet = []
time_sim = []

for i in range(0, num_measurements):
    time_sim.append(i)
    if ranges_avg_feet[i] < 40:
        cleaned_avg_feet.append(ranges_avg_feet[i])
    else:
        cleaned_avg_feet.append(0)

with open('dummy.txt', 'w') as f:
    for i in range(1, len(time_sim)):
        f.write("{}\n".format(cleaned_avg_feet[i]))
    f.close()

print(len(ranges_avg_feet))


plt.ylim(0,40)

fig, ax = plt.subplots()
empty_string_labels = ['']*len(time_sim)
ax.set_xticklabels(empty_string_labels)

plt.plot(time_sim,ranges_avg_feet)
# plt.axes([0,0,len(time_sim),20])
plt.title("Distance between two nodes over time")
plt.xlabel("Time")
plt.ylabel("Measurement (ft)")
plt.grid(False)
plt.show()
# "C:/git/EoEL-Study-Visualization/Plots/1217.png",
