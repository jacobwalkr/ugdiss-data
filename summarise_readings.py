import numpy as np
from datetime import datetime

headers = [
    'room',
    'time',
    'duration (s)',
    'sd(x)',
    'median(x)',
    'range(x)',
    'sd(y)',
    'median(y)',
    'range(y)',
    'sd(z)',
    'median(z)',
    'range(z)',
]

headers_with_details = [
    'room',
    'time',
    'duration (s)',
    'sd(x)',
    'median(x)',
    'range(x)',
    'sd(y)',
    'median(y)',
    'range(y)',
    'sd(z)',
    'median(z)',
    'range(z)',
    'device position',
    'activity nearby',
]

def strip_file_line(line):
    """ Strips the usual suspects from mflog lines """
    return line.strip('# \n')

def stats_vals(values):
    """ Returns a dictionary of standard deviation (std), mean, median and range """
    return {
        'std': np.std(values, ddof=1),
        'mean': np.mean(values),
        'median': np.median(values),
        'range': np.max(values) - np.min(values),
    }

def summarise_file(filename):
    """ Returns a dictionary of useful information and statistical measures from the given
        mflog file
    """
    summary = {}
    preamble = open(filename, 'r').readlines()[:5] # includes first data line
    x, y, z = np.loadtxt(filename, usecols=(1, 2, 3), unpack=True)

    # Room
    summary['room'] = strip_file_line(preamble[0])

    # Time
    summary['time'] = datetime.strptime(preamble[4].split(' ')[0], '%Y-%m-%dT%H:%M:%S.%f')
    summary['time_string'] = summary['time'].strftime('%H:%M:%S, %d %b %y')

    # Duration
    summary['duration'] = strip_file_line(preamble[3])

    # x
    summary['x'] = stats_vals(x)
    summary['y'] = stats_vals(y)
    summary['z'] = stats_vals(z)

    # Text fields
    summary['location'] = strip_file_line(preamble[1])
    summary['activity'] = strip_file_line(preamble[2])

    return summary

# pylint assumes that all "module-level" variables are constants
# pylint: disable=C0103
if __name__ == '__main__':
    import tabulate, sys
    data_rows = []

    first = True
    for filename in sorted(sys.argv[1:]):
        if not first:
            print("\n")
        else:
            first = False

        summary = summarise_file(filename)

        print("[{}]".format(filename))
        print("in {} at {} for {}".format(
            summary['room'],
            summary['time_string'],
            summary['duration']))
        print("Location detail: " + summary['location'])
        print("Activity: " + summary['activity'])
        print()

        dimensions = []

        for dimension in ['x', 'y', 'z']:
            dimensions.append([
                dimension,
                summary[dimension]['std'],
                summary[dimension]['median'],
                summary[dimension]['range']])

        print(tabulate.tabulate(dimensions, headers=['', 'std', 'median', 'range']))
