import os
import sys
import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import mflog_utils

TEST_RUN_NUMBER = 3

# all data from each coordinate
prior_data = {}
prior_files_meta = []
post_data = {}
post_file_meta = {}

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
    
    if run_number == TEST_RUN_NUMBER:
        for file in filenames:
            summary, data = mflog_utils.summarise_file(os.path.join(dirpath, file), True)

            # guaranteed only once
            post_data[summary['location']] = data

            if summary['location'] == '0,0': # first point
                post_file_meta = {
                    'activity': summary['room'],
                    'time_string': summary['time_string']
                }
    else:
        for file in filenames:
            summary, data = mflog_utils.summarise_file(os.path.join(dirpath, file), True)
            coords = summary['location']

            if coords not in prior_data:
                prior_data[coords] = data
            else:
                prior_data[coords] = np.append(prior_data[coords], data, axis=0)

            if coords == '0,0': # first point
                prior_files_meta.append({
                    'activity': summary['room'],
                    'time_string': summary['time_string']
                })

print('Got {} runs'.format(run_number + 1))

# matplotlib setup
mpl.rc('font', family='Arial')
plt.style.use('ggplot')

fig, ax = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
ax[-1].set_xlabel('Position on path around robot arena', size='xx-large')

# Want a nice order (a zig-zag congruous path over the robot arena)
order = ['0,0', '0,1', '0,2', '0,3',
         '1,3', '1,2', '1,1', '1,0',
         '2,0', '2,1', '2,2', '2,3',
         '3,3', '3,2', '3,1', '3,0']

dims = ['x', 'y', 'z']

maxes = np.zeros((16, 3))
mins = np.zeros((16, 3))
means = np.zeros((16, 3))
post_medians = np.zeros((16, 3))

for coord_idx, coords in enumerate(order):
    maxes[coord_idx, :] = np.max(prior_data[coords], axis=0)
    mins[coord_idx, :] = np.min(prior_data[coords], axis=0)
    means[coord_idx, :] = np.mean(prior_data[coords], axis=0)
    post_medians[coord_idx, :] = np.median(post_data[coords], axis=0)

# move the range "bracket" towards the x-axis with the means
means_diff = np.insert(np.diff(means, axis=0), 0, 0, axis=0)
#maxes_diff = np.insert(np.diff(maxes, axis=0), 0, 0, axis=0)
#mins_diff = np.insert(np.diff(mins, axis=0), 0, 0, axis=0)
maxes_diff = maxes - (means - means_diff)
mins_diff = mins - (means - means_diff)
post_medians_diff = np.insert(np.diff(post_medians, axis=0), 0, 0, axis=0)

for dim_idx, dim in enumerate(dims):
    ax[dim_idx].fill_between(range(16), maxes_diff[:, dim_idx], mins_diff[:, dim_idx],
        interpolate=False, color=mflog_utils.tableau20[0])
    ax[dim_idx].plot(range(16), post_medians_diff[:, dim_idx], color=mflog_utils.tableau20[2],
        marker='.', markersize=8, linewidth=2)

    # beautify
    ax[dim_idx].set_xlim((0, 15))
    ax[dim_idx].set_xticks(range(16))
    ax[dim_idx].grid(True, which='major', axis='x')
    ax[dim_idx].tick_params(axis='both', labelsize=14)

fig.tight_layout()

# Write to file
plt.savefig(sys.argv[1] + '.png')

# Write meta to file
with open(sys.argv[1] + '.txt', 'w') as file:
    file.write("Generated: {} from file taken in Computer Room 3's robot arena\n\n"
        .format(datetime.datetime.now().strftime('%c')))

    file.write('# Data used for blue range plot:\n')
    for prior_meta in prior_files_meta:
        file.write('\nData taken at ' + prior_meta['time_string'] + '\n')
        file.write('Activity: ' + prior_meta['activity'] + '\n')

    file.write('\n# Data used for test plot:\n')
    file.write('\nData taken at ' + post_file_meta['time_string'] + '\n')
    file.write('Activity: ' + post_file_meta['activity'] + '\n')

plt.show()


