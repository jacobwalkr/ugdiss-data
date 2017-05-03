import sys
import os
import mflog_utils
import numpy as np
import tabulate

ref_folders = ['RobotArena/{0}/'.format(run) for run in sys.argv[1].strip().split(',')]

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
#ref_diff = np.insert(np.diff(ref_data, axis=1), 0, 0, axis=1)
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

#test_diff = np.insert(np.diff(test_data, axis=0), 0, 0, axis=0)
test_diff = np.diff(test_data, axis=0)

#=================================================================================================#
# Run through tests and find closest diff                                                         #
#=================================================================================================#
def localise_test_path(ref_path, test_path):
    """ Returns the index of the "winning" end-point by testing paths to 5 closest end-points """
    test_len, _ = np.shape(test_path)
    
    # sort by Euclidean distance to the test point for last 5 points
    initial_distances = np.linalg.norm(ref_path - test_path[-1,:], axis=1)
    by_distance = np.argsort(initial_distances)
    
    # discount first <test_len - 1> points and take best 5
    # this could be simplified but we need to retain original indices for getting the right label
    by_distance = by_distance[by_distance >= (test_len - 1)][:5]

    # list of starting points: (<list of Euclidean distances for this path>, <end point>)
    points = [(initial_distances[index], index) for index in by_distance]
    print(ROUTE[min(points)[1] + 1])

    # add the distances for the second item in the path, then third, then fourth and so on
    for step in range(1, test_len):
        for i, (point_sums, point_index) in enumerate(points):
            # step backwards in the paths
            next_ref_index = point_index - 1
            next_test_index = test_len - step

            # new distances
            this_distance = np.linalg.norm(ref_path[next_ref_index] - test_path[next_test_index,:])

            # update
            points[i] = (point_sums + this_distance, point_index)
        print(ROUTE[min(points)[1] + 1])

    return min(points)[1]

test_path_len = int(sys.argv[3])
results = []

# snake along the route through the robot arena
# each point z_k actually represents the difference from z_{k-1} to z_k
for final_node in range(test_path_len, len(ROUTE)):
    # build slice for test path
    first_edge = final_node - test_path_len
    #print(first_edge, final_node)
    test_path = test_diff[first_edge:final_node]

    # localise
    #print(test_path)
    winning_end_point = localise_test_path(ref_diff, test_path)

    # apply labels
    print(ROUTE[winning_end_point + 1] + '\n')
    results.append((ROUTE[final_node], ROUTE[winning_end_point + 1]))

print(tabulate.tabulate(sorted(results), headers=('Test', 'Closest match')))
