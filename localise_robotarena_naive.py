import sys
import os
import mflog_utils
import numpy as np
import tabulate

training_folders = ['RobotArena/{0}/'.format(run) for run in sys.argv[1].strip().split(',')]
test_folders = ['RobotArena/{0}/'.format(run) for run in sys.argv[2].strip().split(',')]

#=================================================================================================#
# Prepare "training" data. Not strictly "training" data but I'm not sure what else to call it     #
#=================================================================================================#
training_files = []

for training_folder in training_folders:
    training_files += [training_folder + f for f in os.listdir(training_folder)
        if os.path.isfile(os.path.join(training_folder, f))]

labels = [] # plain python list
arg_labels = np.empty(len(training_files), dtype=np.int32) # medium for argsorting labels
training_data = np.zeros((len(training_folders) * 16, 3))

for i, filename in enumerate(training_files):
    summary = mflog_utils.summarise_file(filename)
    labels.append(summary['location'])
    arg_labels[i] = i
    xm = summary['x']['median']
    ym = summary['y']['median']
    zm = summary['z']['median']
    training_data[i, :] = [xm, ym, zm]

#=================================================================================================#
# Run through test files and compare them to "training" data                                      #
#=================================================================================================#
test_files = []

for test_folder in test_folders:
    test_files += [test_folder + f for f in os.listdir(test_folder)
        if os.path.isfile(os.path.join(test_folder, f))]

results = []

for i, filename in enumerate(test_files):
    test_summary = mflog_utils.summarise_file(filename)
    test_location = test_summary['location']
    test_data = np.array([
        test_summary['x']['median'],
        test_summary['y']['median'],
        test_summary['z']['median'],
    ])

    # vectors representing Euclidean distance to test point
    distances = np.linalg.norm(training_data - test_data, axis=1)

    # get the closest point and find its label
    min_idx = np.argmin(distances)
    result_location = labels[arg_labels[min_idx]]
    results.append((test_location, result_location))

#print('\n'.join([test + ';' + result for test, result in results]))
print(tabulate.tabulate(results, headers=('Test', 'Closest match')))
