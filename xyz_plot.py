import sys
import matplotlib
import matplotlib.pyplot as plt
from mflog_utils import extract_data_from_file, stats_vals

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

def draw_xyz_plot(files, save=None):
    """ Draws a grid of plots, with a row for each file's x, y and z dimensions. `files` is a
        string list of names of .mflog files. If `save` is given and is a string, the plot is
        saved to `save`.
    """
    matplotlib.rc('font', family='Arial', weight='bold')
    plt.style.use('ggplot')

    figure, axes = plt.subplots(len(files), 3, sharex='col', figsize=(12, 3*len(files)),
        squeeze=False)

    axes[0, 0].set_title('x', size='xx-large', position=[0.5, 1.05])
    axes[0, 1].set_title('y', size='xx-large', position=[0.5, 1.05])
    axes[0, 2].set_title('z', size='xx-large', position=[0.5, 1.05])

    axes[-1, 0].set_xlabel(u'μT', fontweight='bold')
    axes[-1, 1].set_xlabel(u'μT', fontweight='bold')
    axes[-1, 2].set_xlabel(u'μT', fontweight='bold')

    for (file_index, file_name) in enumerate(files):
        data = extract_data_from_file(file_name).T
        axes[file_index, 0].set_ylabel('L' + str(file_index), rotation=0, size='xx-large',
            labelpad=40)

        for dimension in range(3):
            these_axes = axes[file_index, dimension]
            these_axes.tick_params(
                axis='y',
                which='both',
                left='off',
                right='off',
                labelleft='off'
            )

            these_axes.get_xaxis().tick_bottom()
            #these_axes.get_yaxis().tick_left()

            # Good to disable spines in default style
            # these_axes.spines["top"].set_visible(False)
            # #these_axes.spines["bottom"].set_visible(False)
            # these_axes.spines["right"].set_visible(False)
            # these_axes.spines["left"].set_visible(False)

            these_axes.hist(data[dimension], 25, normed=1, color=tableau20[0::2][file_index % 20])

    figure.tight_layout()

    if isinstance(save, str):
        plt.savefig(save) # woo, duck typing

    plt.show()

if __name__ == '__main__':
    """ Takes at least one mflog filenames as argument, with the final argument being the filename
        to save the resulting plot to.
    """
    files = sys.argv[1:-1]

    if len(files) > 0:
        draw_xyz_plot(files, save=sys.argv[-1])#, save='plot.png')
    else:
        print('Expected list of files, got: ' + str(files))
