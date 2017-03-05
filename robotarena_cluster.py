import os
from itertools import cycle
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mflog_utils

mpl.rc('font', family='Arial', weight='bold')
#plt.style.use('ggplot')

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X', size='xx-large')
ax.set_ylabel('Y', size='xx-large')
ax.set_zlabel('Z', size='xx-large')

summaries = {}

# Read in input files
for dirpath, _, filenames in os.walk('RobotArena'):
    for file in filenames:
        summary = mflog_utils.summarise_file(os.path.join(dirpath, file))
        coords = summary['location']

        #print(summaries)
        if coords in summaries:
            summaries[coords].append(summary)
        else:
            summaries[coords] = [summary]

colours = cycle(mflog_utils.tableau20)
for location in summaries.values():
    colour = next(colours)
    location_points = []

    for summary in location:
        medians = [summary[d]['median'] for d in 'xyz']
        ax.scatter(*medians, color=colour, s=30)
        location_points.append(medians)

    ax.plot(*zip(*location_points), color=colour)

fig.tight_layout()
plt.savefig('Plots/RobotArena012_scatter.png')
plt.show()
