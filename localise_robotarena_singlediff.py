import sys
import os
import mflog_utils
import numpy as np
import tabulate

ref_folders = ['RobotArena/{0}/'.format(run) for run in sys.argv[1].strip().split(',')]
#test_folders = ['RobotArena/{0}/'.format(run) for run in sys.argv[2].strip().split(',')]

ROUTE = np.array([
    '0,0',
    '0,1',
    '0,2',
    '0,3',
    '1,3',
    '1,2',
    '1,1',
    '1,0',
    '2,0',
    '2,1',
    '2,2',
    '2,3',
    '3,3',
    '3,2',
    '3,1',
    '3,0',
])

#=================================================================================================#
# Prepare reference data.                                                                         #
#=================================================================================================#
#ref_folder = 'RobotArena/{0}/'.format(sys.argv[1].strip())

ref_data = np.zeros((len(ref_folders), len(ROUTE), 3))

# stack the route from each folder up along the 3rd axis
for repeat, ref_folder in enumerate(ref_folders):
    for filename in os.listdir(ref_folder):
        file_path = os.path.join(ref_folder, filename)
        if os.path.isfile(file_path): # no folders (just in case)
            summary = mflog_utils.summarise_file(file_path)

            # put the data in this file at the right position along the route
            index = np.where(ROUTE == summary['location'])

            ref_data[repeat, index, :] = [
                summary['x']['median'],
                summary['y']['median'],
                summary['z']['median'],
            ]

# take the diff of each repeat at once and take their mean
# ref_diff = np.insert(np.diff(ref_data, axis=1), 0, 0, axis=1)
ref_diff = np.diff(ref_data, axis=1)
ref_diff = np.mean(ref_diff, axis=0)

#=================================================================================================#
# Produce test set                                                                                #
#=================================================================================================#
test_folder = 'RobotArena/{0}/'.format(sys.argv[2].strip())
test_files = []

test_files += [test_folder + f for f in os.listdir(test_folder)
    if os.path.isfile(os.path.join(test_folder, f))]

test_data = np.zeros((16, 3))

# prepare test diffs
for i, filename in enumerate(test_files):
    test_summary = mflog_utils.summarise_file(filename)
    index = np.where(ROUTE == test_summary['location'])
    test_data[index, :] = [
        test_summary['x']['median'],
        test_summary['y']['median'],
        test_summary['z']['median'],
    ]

# test_diffs = np.insert(np.diff(test_data, axis=0), 0, 0, axis=0)
test_diffs = np.diff(test_data, axis=0)

#=================================================================================================#
# Run through tests and find closest diff                                                         #
#=================================================================================================#
results = []

for i, test_point in enumerate(test_diffs):
    # find distances to ref points
    distances = np.linalg.norm(ref_diff - test_point, axis=1)

    # match labels and append to results
    results.append((ROUTE[i + 1], ROUTE[np.argmin(distances) + 1]))

print(tabulate.tabulate(sorted(results), headers=('Test', 'Closest match')))
