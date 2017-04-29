""" Draws a 3D plot representing the magnetic field at each spot on the 4x4 grid drawn on the
    robot arena in the Diamond's Computer Room 3.
"""
import sys
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # pylint: disable=W0611
import mpl_toolkits.mplot3d.art3d as art3d
import mflog_utils
import datetime

search_dir = sys.argv[1] # will look like an integer - in ./RobotArena/*
output_fn = sys.argv[2]
files = []

for dirpath, _, filenames in os.walk(search_dir):
    files += [os.path.join(dirpath, fn) for fn in filenames]
    break

if len(files) != 16:
    print('Expected 16 files, found ' + len(files))
    sys.exit(1)

SPOT_SPACING = 780 # millimetres
SPOT_RADIUS = 150 # millimetres
ARENA_SIZE = SPOT_SPACING * 5
CIRCLE_RED = (232./255., 46./255., 9./255.)
CIRCLE_GREEN = (41./255., 179./255., 75./255.)
CIRCLE_BLUE = (7./255., 107./255., 237./255.)
CIRCLE_YELLOW = (247./255., 211./255., 5./255.)

# A list of coordinates (x, y) of spots, allowing a space of SPOT_SPACING mm
# around the edges. Ordered from bottom left in row-major form.
SPOT_POSITIONS = [(x * SPOT_SPACING, y * SPOT_SPACING)
    for x in range(1, 5) for y in range(1, 5)]

# The colour of each spot in the same order as above
SPOT_COLOURS = [
    CIRCLE_BLUE, CIRCLE_RED, CIRCLE_YELLOW, CIRCLE_GREEN,
    CIRCLE_YELLOW, CIRCLE_GREEN, CIRCLE_BLUE, CIRCLE_RED,
    CIRCLE_RED, CIRCLE_BLUE, CIRCLE_GREEN, CIRCLE_YELLOW,
    CIRCLE_GREEN, CIRCLE_YELLOW, CIRCLE_RED, CIRCLE_BLUE,
]

# How much to multiply magnetic readings by in the final plot (because they're in microtesla and
# the plot scale is in millimetres)
MAGNETIC_SCALE_FACTOR = 1

mpl.rc('font', family='Arial', weight='bold')
#plt.style.use('ggplot')

figure = plt.figure(figsize=(12, 9))
ax = figure.add_subplot(111, projection='3d')
ax.set_xlim([0, ARENA_SIZE])
ax.set_ylim([0, ARENA_SIZE])
ax.set_zlim([-ARENA_SIZE, 0])
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.zaxis.set_ticklabels([])

for spot_detail in zip(SPOT_POSITIONS, SPOT_COLOURS):
    spot = mpl.patches.Circle(spot_detail[0], SPOT_RADIUS, color=spot_detail[1], zorder=0)
    ax.add_patch(spot)
    art3d.patch_2d_to_3d(spot, z=0)

# Read files
arrow_magnitudes = np.zeros((16, 3))
arrow_positions = np.zeros((16, 3))
arrows = None # for now
first_file_activity = ''
first_file_datetime = ''
first_file_filename = ''

for file in files:
    # pylint: disable=invalid-sequence-index
    summary = mflog_utils.summarise_file(file)

    # The location of arena files is set to "x,y" where x and y are integers between 0 and 3
    locx, locy = summary['location'].split(',', 1)
    locx = int(locx)
    locy = int(locy)

    if locx == 0 and locy == 0:
        # The first file!
        first_file_activity = summary['activity']
        first_file_datetime = summary['time_string']
        first_file_filename = file.split('/')[-1].split('.')[0]

    # Get the position of this arrow in the same order as the spots
    ordinal = locy * 4 + locx

    arrow_positions[ordinal] = np.array([*SPOT_POSITIONS[ordinal], 0]).reshape((1, 3))

    arrow_magnitudes[ordinal] = np.array([
        summary['x']['mean'],
        summary['y']['mean'],
        summary['z']['mean'],
    ]).reshape((1, 3)) * MAGNETIC_SCALE_FACTOR

arrows = np.concatenate((arrow_positions, arrow_magnitudes), axis=1)
plt.quiver(*arrows.T, color='black', length=3000, pivot='tail', zorder=100)
figure.tight_layout()

# so all the arrows for RobotArena/0/* show on screen
ax.azim = -20
ax.elev = 35

plt.savefig('{}.png'.format(output_fn))

# Write meta file
with open('{}.txt'.format(output_fn), 'w') as metafile:
    metafile.write('Generated: {}\n\n'.format(datetime.datetime.now().strftime('%c')))
    metafile.write('Readings taken from the robot arena in the Diamond Computer Room 3 at '
        + first_file_datetime + '\n')
    metafile.write('Activity: ' + first_file_activity + '\n')

plt.show()
