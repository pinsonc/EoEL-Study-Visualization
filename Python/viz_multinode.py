import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics
import time
import os
from datetime import datetime


path = 'C:/Users/pinso/Downloads/Lab Test 1/test1012/DATA2B_20191012.LOG'
node1id = '2c'
node2id = '2d'

timestamp1 = []
timestamp2 = []
measurement1 = []
measurement2 = []

# get one list of timestamps and one list of measurements
i = 0
with open(path) as f:
    line_count = 0
    for line in f:
        if line[0] != '#':
            line_list = line.split('\t')
            i += 1
            node_id = line_list[1][-2:]
            if (int(line_list[2].rstrip('\n')) != 0):
                if (node_id == node1id):
                    measurement1.append(int(line_list[2].rstrip('\n')))
                    timestamp1.append(i)
                if (node_id == node2id):
                    measurement2.append(int(line_list[2].rstrip('\n')))
                    timestamp2.append(i)
            

ranges_avg_inch1 = [x / 25.4 for x in measurement1]
ranges_avg_inch2 = [x / 25.4 for x in measurement2]
ranges_avg_feet1 = [x / 12 for x in ranges_avg_inch1]
ranges_avg_feet2 = [x / 12 for x in ranges_avg_inch2]

plt.ylim(0,40)

fig, ax = plt.subplots()
empty_string_labels = ['']*len(timestamp1)
ax.set_xticklabels(empty_string_labels)

plt.plot(timestamp1,ranges_avg_feet1)
plt.plot(timestamp2,ranges_avg_feet2)
plt.title("Distance between two nodes over time")
plt.xlabel("Time")
plt.ylabel("Measurement (ft)")
plt.grid(False)
plt.show()


# "C:/git/EoEL-Study-Visualization/Plots/1217.png",
