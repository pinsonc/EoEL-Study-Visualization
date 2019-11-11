import numpy as np
import matplotlib.pyplot as plt

# Function to parse text file and create lists of each interaction type
def parse_input():
    f = np.loadtxt("feet/feet_DATA2B_20191010_Test2.txt")
    count = 0
    totalCount = 0

    # Keeps track of consecutive measurements -> if there are 10 consecutive
    # measurements in a row that were in touching distance, touching variable would be of value 10
    touching = 0
    arm = 0
    room = 0
    far = 0

    # Lists that contain different number of consecutive measurements recorded in test -> if there were 12, 34, and
    # 45 consecutive measurements then arm_length would be [12, 34, 45]. These are used to determine average time
    # and total time for each interaction

    touching_distance = []
    arm_length = []
    same_room = []
    no_interaction = []

    i = 0
    while i < len(f):
        totalCount = totalCount + 1
        if f[i] < 1:
            while i < len(f) and f[i] <= 1:
                touching += 1
                totalCount += 1
                i += 1

            touching_distance.append(touching)
            touching = 0
        elif f[i] < 3:
            while i < len(f) and f[i] <= 3 and f[i] > 1:
                arm += 1
                totalCount += 1
                i += 1

            arm_length.append(arm)
            arm = 0
        elif f[i] < 10:
            while i < len(f) and f[i] <= 10 and f[i] > 3:
                room += 1
                totalCount += 1
                i += 1

            same_room.append(room)
            room = 0
        elif f[i] > 10:
            while i < len(f) and f[i] > 10:
                far += 1
                totalCount += 1
                i += 1

            no_interaction.append(far)
            far = 0
        else:
            i += 1

    print(len(touching_distance), len(arm_length), len(same_room), len(no_interaction))
    print(sum(touching_distance) + sum(arm_length) + sum(same_room) + sum(no_interaction))
    return (f, touching_distance, arm_length, same_room, no_interaction)


def plot(f, touching_distance, arm_length, same_room, no_interaction):
    objects = ('Touching Distance', 'Arm Length', 'Same Room', 'No interaction')
    y_pos = np.arange(len(objects))
    avg_time = [sum(touching_distance) / len(touching_distance), sum(arm_length) / len(arm_length),
                sum(same_room) / len(same_room), sum(no_interaction) / len(no_interaction)]


    # Simple bar plot displaying data
    bins = [0, 1, 2, 3, 4, 5, 6 , 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    plt.hist(f, bins=bins)
    plt.xlabel('Distance(ft)')
    plt.ylabel('Number of Measurements')
    plt.title('Frequency of Measurements')
    plt.show()

    # Average Time Duration for each Interaction Type
    plt.bar(y_pos, avg_time, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Interaction Type')
    plt.ylabel('Average Time (seconds)')
    plt.title('Time Duration per Interaction Type')
    plt.show()

    # Frequency of measurements (if in one particular bin for 30 measurements, only consider that frequency of 1)
    y_val = [len(touching_distance), len(arm_length), len(same_room), len(no_interaction)]
    plt.bar(y_pos, y_val, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Interaction Type')
    plt.ylabel('Average Number of Measurements')
    plt.title('Frequency per Interaction Type')
    plt.show()

    # Pie Chart Visualization
    interaction_count = [sum(touching_distance), sum(arm_length), sum(same_room), sum(no_interaction)]
    interaction_typ = ['Touching Distance', 'Arm Length', 'Same Room', 'No Interaction']
    colors = ['lightcoral', 'yellowgreen', 'lightskyblue', 'gold']
    patches, texts = plt.pie(interaction_count, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, interaction_typ, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    my_circle = plt.Circle((0, 0), 0.7, color='white')
    plt.pie(interaction_count, labels=interaction_typ, colors=colors, wedgeprops={'linewidth': 7, 'edgecolor': 'white'})
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.show()


f, touching_distance, arm_length, same_room, no_interaction = parse_input()
plot(f, touching_distance, arm_length, same_room, no_interaction)
