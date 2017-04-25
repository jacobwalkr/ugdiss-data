import os
import numpy as np
import mflog_utils
import tabulate

def count_uniques(subject):
    """ Returns a numpy array containing only unique elements from subject """
    return len({tuple(row) for row in subject})

files = []

for dirpath, _, filenames in os.walk('./FrequencyTesting'):
    for filename in filenames:
        if filename.endswith('.mflog'):
            files.append(os.path.join(dirpath, filename))

    break

tests = []

for filename in files:
    summary, data = mflog_utils.summarise_file(filename, True)
    num_unique = count_uniques(data)
    tests.append([summary['frequency_label'], summary['sample_count'],
        (num_unique / summary['sample_count']) * 100, summary['x']['range'], summary['x']['std']**2])

print(tabulate.tabulate(tests,
    headers=('SENSOR_DELAY_*', 'Samples', '\% unique', 'Range', 'Var(x)')))

with open('./FrequencyTesting/summary.csv', 'w') as out:
    for test in tests:
        out.write(','.join([str(t) for t in test]) + '\n')
