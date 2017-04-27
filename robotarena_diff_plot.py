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

# run numbers to use
run_numbers = [int(num) for num in sys.argv[1:-1]]

for run_number in run_numbers:
    for dirpath, _, filenames in os.walk('RobotArena/' + str(run_number)):
        # Yay, order!
        print('Doing run #' + str(run_number))
        summaries[run_number] = {}

        for file in filenames:
            summary = mflog_utils.summarise_file(os.path.join(dirpath, file))
            summaries[run_number][summary['location']] = summary

        # just the once - no subdirs
        break

print('Got {} runs'.format(len(summaries)))

# matplotlib setup
mpl.rc('font', family='Arial')
#plt.style.use('ggplot')

fig, ax = plt.subplots(len(summaries), 3, figsize=(15, 2.5 * len(summaries) + 2), squeeze=False,
    sharex='col', sharey='row')
ax[-1, 1].set_xlabel('Position on path around robot arena', size='x-large')
ax[0, 0].set_title('x', fontsize=16)
ax[0, 1].set_title('y', fontsize=16)
ax[0, 2].set_title('z', fontsize=16)

# Want a nice order (a zig-zag congruous path over the robot arena)
order = ['0,0', '0,1', '0,2', '0,3',
         '1,3', '1,2', '1,1', '1,0',
         '2,0', '2,1', '2,2', '2,3',
         '3,3', '3,2', '3,1', '3,0']

# bright colours then light colours
colours = mflog_utils.tableau20[0::2] + mflog_utils.tableau20[1::2]

for run_number, run in sorted(summaries.items()):
    run_data = np.zeros((3, 16))

    for i, coords in enumerate(order):
        run_data[:,i] = [
            run[coords]['x']['median'],
            run[coords]['y']['median'],
            run[coords]['z']['median'],
        ]

    # Calculate a moving difference and add the first item (always zero) back in
    run_data = np.insert(np.diff(run_data), 0, 0, axis=1)

    # Plot
    for dimension in [0, 1, 2]: # 0 is x, 1 is y, 2 is z
        ax[run_number, dimension].plot(range(0, 16), run_data[dimension],
            color=colours[run_number], marker='.', markersize=8, linewidth=2)
        
        # beautify
        ax[run_number, dimension].set_xlim((0, 15))
        ax[run_number, dimension].set_xticks(range(0, 16, 2))
        ax[run_number, dimension].grid(True, which='major', axis='both')
        ax[run_number, dimension].tick_params(axis='both', labelsize=18)

    # beautify
    ax[run_number, 0].set_ylabel(u'R{} (Δ μT)'.format(str(run_number)), rotation=0, size='x-large',
        labelpad=40)

fig.tight_layout()

# Write to file
plt.savefig(sys.argv[-1] + '.png')

# Write meta to file
with open(sys.argv[-1] + '.txt', 'w') as file:
    file.write('Generated: {}\n'.format(datetime.datetime.now().strftime('%c')))

    for run_number, runs in summaries.items():
        file.write('\n')
        file.write('{}{}: {} at {}\n'.format('R', str(run_number), runs['0,0']['room'],
            runs['0,0']['time_string']))
        file.write('Activity: {}\n'.format(runs['0,0']['activity']))

# Go time
plt.show()
