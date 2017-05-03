import os
import numpy as np
import mflog_utils
import tabulate

files = []

for dirpath, _, filenames in os.walk('./TimeTesting'):
    for filename in filenames:
        if filename.endswith('.mflog'):
            files.append(os.path.join(dirpath, filename))

    break

tests = []

for filename in files:
    summary, data = mflog_utils.summarise_file(filename, True)
    tests.append([summary['duration'], summary['sample_count'], summary['x']['median'],
        summary['x']['range'], summary['x']['std']**2])

tests.sort()
print(tabulate.tabulate(tests,
    headers=('Duration', 'Samples', 'Median (x)', 'Range (x)', 'Var (x)')))

with open('./TimeTesting/summary.csv', 'w') as out:
    for test in tests:
        out.write(','.join([str(t) for t in test]) + '\n')
