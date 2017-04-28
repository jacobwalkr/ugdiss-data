import sys
import os
import mflog_utils
import numpy as np

#=================================================================================================#
# Prepare "training" data. Not strictly "training" data but I'm not sure what else to call it     #
#=================================================================================================#
training_files = [
    'Tranche1-Jan27/0201-ComputerRoom3_2017-01-27_17-30-59.mflog',
    'Tranche1-Jan27/0201-StudyBalcony_2017-01-27_16-43-34.mflog',
    'Tranche1-Jan27/0302-IndividualStudy_2017-01-27_17-05-33.mflog',
    'Tranche1-Jan27/0304-Corridor_2017-01-27_17-13-54.mflog',
    'Tranche2-Feb03/0101-Moonscape_2017-02-03_20-07-34.mflog',
]

labels = [] # plain python list
arg_labels = np.empty(len(training_files), dtype=np.int32) # medium for argsorting labels
training_data = np.zeros((16, 3))

for i, filename in enumerate(training_files):
    summary = mflog_utils.summarise_file(filename)
    labels.append(summary['room'])
    arg_labels[i] = i
    xm = summary['x']['median']
    ym = summary['y']['median']
    zm = summary['z']['median']
    training_data[i, :] = [xm, ym, zm]

#=================================================================================================#
# Run through test files and compare them to "training" data                                      #
#=================================================================================================#
test_files = [
    'Tranche2-Feb03/0201-ComputerRoom3_2017-02-03_19-52-37.mflog',
    'Tranche2-Feb03/0201-StudyBalcony_2017-02-03_19-46-02.mflog',
    'Tranche2-Feb03/0302-IndividualStudy_2017-02-03_19-30-26.mflog',
    'Tranche2-Feb03/0304-Corridor_2017-02-03_19-38-58.mflog',
    'Tranche6-Apr26/0101-Moonscape_2017-04-25_22-49-46.mflog',
]

for i, filename in enumerate(test_files):
    test_summary = mflog_utils.summarise_file(filename)
    test_room = test_summary['room']
    test_data = np.array([
        test_summary['x']['median'],
        test_summary['y']['median'],
        test_summary['z']['median'],
    ])

    # vectors representing Euclidean distance to test point
    distances = np.linalg.norm(training_data - test_data, axis=1)

    # get the closest point and find its label
    min_idx = np.argmin(distances)
    result_room = labels[arg_labels[min_idx]]
    print('Test room: {0}\nResult: {1}\n'.format(test_room, result_room))
