import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics
import time
import os
from datetime import datetime


directory = os.fsencode('C:/Users/pinso/Downloads/Lab Test 1/test1012/')

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".LOG"): 
        print(filename)

        timestamp = []
        measurement = []

        # get one list of timestamps and one list of measurements
        i = 0
        with open(os.fsdecode(directory) + "/" + filename) as f:
            line_count = 0
            for line in f:
                if line[0] != '#':
                    line_list = line.split('\t')
                    timestamp.append(i)
                    i += 1
                    measurement.append(int(line_list[2].rstrip('\n')))

        ranges_avg_inch = [x / 25.4 for x in measurement]
        ranges_avg_feet = [x / 12 for x in ranges_avg_inch]

        cleaned_avg_feet = []
        time_sim = []

        '''
        for i in range(0, len(timestamp)):
            time_sim.append(i)
            if ranges_avg_feet[i] < 40:
                cleaned_avg_feet.append(ranges_avg_feet[i])
            else:
                cleaned_avg_feet.append(0)
        '''

        with open('feet/feet_{}.txt'.format(filename[:-4]), 'w') as f:
            for i in range(1, len(time_sim)):
                f.write("{}\n".format(ranges_avg_feet[i]))
            f.close()

        with open('stats/stats_{}.txt'.format(filename[:-4]), 'w') as f:
            f.write('Number of measurements: {}'.format(len(ranges_avg_feet)))

        plt.ylim(0,40)

        fig, ax = plt.subplots()
        empty_string_labels = ['']*len(time_sim)
        ax.set_xticklabels(empty_string_labels)

        plt.plot(timestamp,ranges_avg_feet)
        plt.title("Distance between two nodes over time")
        plt.xlabel("Time")
        plt.ylabel("Measurement (ft)")
        plt.grid(False)
        plt.savefig('figs/fig_{}.png'.format(filename[:-4]))
    else:
        continue


        # "C:/git/EoEL-Study-Visualization/Plots/1217.png",
