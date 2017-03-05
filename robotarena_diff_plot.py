import os
import sys
import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import mflog_utils

summaries = {}

# Read mflog files
for dirpath, _, filenames in os.walk('RobotArena'):
    # Assuming we never revisit the same directory
    dirpath_parts = list(filter(None, dirpath.split('\\')))

    # First item yielded by walk is just the "RobotArena" directory. No want.
    if len(dirpath_parts) < 2:
        continue
    else:
        run_number = int(dirpath_parts[1])

    # Yay, order!
    print('Doing run #' + str(run_number))
    summaries[run_number] = {}

    for file in filenames:
        summary = mflog_utils.summarise_file(os.path.join(dirpath, file))
        summaries[run_number][summary['location']] = summary

print('Got {} runs'.format(len(summaries)))

# matplotlib setup
mpl.rc('font', family='Arial', weight='bold')
plt.style.use('ggplot')

fig, ax = plt.subplots(len(summaries), 1, figsize=(12, 3 * len(summaries) + 2), squeeze=False,
    sharex='col')
ax[-1, 0].set_xlabel(u'Position on path around robot arena', size='x-large')

# Three of the brighter colours from Tableau
# TODO: Adapt for more than 3 sets of readings
colour_trio = [mflog_utils.tableau20[c] for c in [0, 2, 6]]

# Want a nice order (a zig-zag congruous path over the robot arena)
order = ['0,0', '0,1', '0,2', '0,3',
         '1,3', '1,2', '1,1', '1,0',
         '2,0', '2,1', '2,2', '2,3',
         '3,3', '3,2', '3,1', '3,0']

for run_number, run in sorted(summaries.items()):
    this_run = np.zeros((3, 16))

    for i, coords in enumerate(order):
        this_run[:,i] = [
            run[coords]['x']['median'],
            run[coords]['y']['median'],
            run[coords]['z']['median'],
        ]

    # Calculate a moving difference and add the first item (always zero) back in
    this_run = np.insert(np.diff(this_run), 0, 0, axis=1)

    # Plot
    for i in [0, 1, 2]: # x is 0, y is 1, z is 2
        ax[run_number, 0].plot(range(0, 16), this_run[i], color=colour_trio[i], marker='.',
            markersize=8, linewidth=2)

    # Make the plot prettier
    ax[run_number, 0].set_ylabel('R{} (Δ μT)'.format(str(run_number)), rotation=0, size='x-large',
        labelpad=40)
    ax[run_number, 0].set_xlim((0, 15))

# Make legend
legend_patches = [
    mpatches.Patch(color=colour_trio[0], label='x axis'),
    mpatches.Patch(color=colour_trio[1], label='y axis'),
    mpatches.Patch(color=colour_trio[2], label='z axis'),
]
# TODO: Need to adapt this figure positioning for more sets of readings
plt.legend(handles=legend_patches, loc="lower left", bbox_to_anchor=(0,0))

# Crop edges of plots to data
plt.xticks(range(0, 16))

fig.tight_layout()

# Write to file
plt.savefig(sys.argv[1] + '.png')

# Write meta to file
with open(sys.argv[1] + '.txt', 'w') as file:
    file.write('Generated: {} in Computer Room 3\n'.format(datetime.datetime.now().strftime('%c')))

    for run_number, runs in summaries.items():
        file.write('\n')
        file.write('{}{}: {} at {}\n'.format('R', str(run_number), runs['0,0']['room'],
            runs['0,0']['time_string']))
        file.write('Activity: {}\n'.format(runs['0,0']['activity']))

# Go time
plt.show()
