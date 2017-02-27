import sys
import matplotlib
import matplotlib.pyplot as plt
import datetime
import mflog_utils

def save_meta_file(filename, file_summaries):
    """ Takes dict of location key -> file summary and writes summaries to filename """
    with open(filename, 'w') as file:
        file.write('Generated: {}\n'.format(datetime.datetime.now().strftime('%c')))

        for key, summary in file_summaries.items():
            file.write('\n')
            file.write('{}: {} at {}\n'.format(key, summary['room'], summary['time_string']))
            file.write('Location details: {}\n'.format(summary['location']))
            file.write('Activity: {}\n'.format(summary['activity']))

def draw_xyz_plot(files, save=None, location_as_label=False, label_prefix='L'):
    """ Draws a grid of plots, with a row for each file's x, y and z dimensions. `files` is a
        string list of names of .mflog files. If `save` is given and is a string, the plot is
        saved to `save`.
    """
    matplotlib.rc('font', family='Arial', weight='bold')
    plt.style.use('ggplot')

    figure, axes = plt.subplots(len(files), 3, sharex='col', figsize=(12, 1*len(files)),
        squeeze=False)

    axes[0, 0].set_title('x', size='xx-large', position=[0.5, 1.05])
    axes[0, 1].set_title('y', size='xx-large', position=[0.5, 1.05])
    axes[0, 2].set_title('z', size='xx-large', position=[0.5, 1.05])

    axes[-1, 0].set_xlabel(u'μT', fontweight='bold')
    axes[-1, 1].set_xlabel(u'μT', fontweight='bold')
    axes[-1, 2].set_xlabel(u'μT', fontweight='bold')

    location_keys = {}

    for (file_index, file_name) in enumerate(files):
        summary, data = mflog_utils.summarise_file(file_name, include_data=True)

        if location_as_label:
            location_key = summary['location']
        else:
            location_key = label_prefix + str(file_index)

        location_keys[location_key] = summary
        axes[file_index, 0].set_ylabel(location_key, rotation=0, size='xx-large',
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

            # these_axes.hist(data.T[dimension], 25, normed=1,
            #     color=mflog_utils.tableau20[0::2][file_index % 10], linewidth=0)
            these_axes.hist(data.T[dimension], 25, normed=1, color='black', linewidth=0)

    figure.tight_layout()

    if isinstance(save, str):
        plt.savefig(save + '.png') # woo, duck typing
        save_meta_file(save + '.txt', location_keys)

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
