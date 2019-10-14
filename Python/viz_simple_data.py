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
i = 0
with open(data_path) as f:
    line_count = 0
    for line in f:
        if line[0] != '#':
            line_list = line.split('\t')
            timestamp.append(i)
            i += 1
            measurement.append(int(line_list[2].rstrip('\n')))

print(len(measurement))

ranges_avg_inch = [x / 25.4 for x in measurement]
ranges_avg_feet = [x / 12 for x in ranges_avg_inch]

print(len(ranges_avg_feet))

cleaned_avg_feet = []
time_sim = []

for i in range(0, len(timestamp)):
    time_sim.append(i)
    if ranges_avg_feet[i] < 40:
        cleaned_avg_feet.append(ranges_avg_feet[i])
    else:
        cleaned_avg_feet.append(0)

with open('dummy.txt', 'w') as f:
    for i in range(1, len(time_sim)):
        f.write("{}\n".format(cleaned_avg_feet[i]))
    f.close()

print(len(cleaned_avg_feet))


plt.ylim(0,40)

fig, ax = plt.subplots()
empty_string_labels = ['']*len(time_sim)
ax.set_xticklabels(empty_string_labels)

plt.plot(time_sim,cleaned_avg_feet)
plt.title("Distance between two nodes over time")
plt.xlabel("Time")
plt.ylabel("Measurement (ft)")
plt.grid(False)
plt.show()
# "C:/git/EoEL-Study-Visualization/Plots/1217.png",
