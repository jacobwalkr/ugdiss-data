""" Convert all given metadata files to a LaTeX table format """
import sys
import os

input_files = sys.argv[1:]

# Format of files is generally:
# -
#0 Generated: <datetime (%c)>
#1 <blank line>
#2 <label>: <room> at <time>, <date>
#3 Location details: <location details>
#4 Activity: <activity>
#5 <blank line>
# <Repeat lines 0-5>
# -

rows = []

for input_fn in input_files:
    with open(input_fn, 'r') as input_file:
        meta_lines = list(input_file)[2:]
        num_meta_groups = int((len(meta_lines) + 1) / 4)

        for meta_group_idx in range(0, num_meta_groups):
            start = meta_group_idx * 4
            meta_group_lines = meta_lines[start:start+4]
            label, details = meta_group_lines[0].strip().split(': ')
            room, date_details = details.split(' at ')
            time, date = date_details.split(', ')

            rows.append([label, room, date, time])

for row in rows:
    print('{0} & {1} & {2} & {3} \\\\'.format(*row))
