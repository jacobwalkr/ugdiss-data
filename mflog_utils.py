import numpy as np
from datetime import datetime

# Colour codes courtesy of Tableau and Randy Olson
# http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
# These are the "Tableau 20" colors as RGB.
tableau20 = [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
    (0.6823529411764706, 0.7803921568627451, 0.9098039215686274),
    (1.0, 0.4980392156862745, 0.054901960784313725),
    (1.0, 0.7333333333333333, 0.47058823529411764),
    (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
    (0.596078431372549, 0.8745098039215686, 0.5411764705882353),
    (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
    (1.0, 0.596078431372549, 0.5882352941176471),
    (0.5803921568627451, 0.403921568627451, 0.7411764705882353),
    (0.7725490196078432, 0.6901960784313725, 0.8352941176470589),
    (0.5490196078431373, 0.33725490196078434, 0.29411764705882354),
    (0.7686274509803922, 0.611764705882353, 0.5803921568627451),
    (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),
    (0.9686274509803922, 0.7137254901960784, 0.8235294117647058),
    (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),
    (0.7803921568627451, 0.7803921568627451, 0.7803921568627451),
    (0.7372549019607844, 0.7411764705882353, 0.13333333333333333),
    (0.8588235294117647, 0.8588235294117647, 0.5529411764705883),
    (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),
    (0.6196078431372549, 0.8549019607843137, 0.8980392156862745)]

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

def extract_data_from_file(filename):
    """ Returns ndarray of x, y, z data from file """
    return np.loadtxt(filename, usecols=(1, 2, 3))

def summarise_file(filename, include_data=False):
    """ Returns a dictionary of useful information and statistical measures from the given
        mflog file
    """
    summary = {}
    preamble = open(filename, 'r').readlines()[:5] # includes first data line
    data = extract_data_from_file(filename)
    x, y, z = data.T

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

    if include_data:
        return summary, data

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
