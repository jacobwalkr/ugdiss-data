import os
import numpy as np
import matplotlib.pyplot as plt
import mflog_utils

def plot_xyz(data, title, save_name):
    len_data, _ = np.shape(data)

    # plot
    fig, ax = plt.subplots(3, 1, sharex='col', figsize=(8, 6))

    ax[0].set_title(title, fontsize=18)

    ax[0].plot(range(0, len_data), data[:,0], color=mflog_utils.tableau20[0])
    ax[1].plot(range(0, len_data), data[:,1], color=mflog_utils.tableau20[2])
    ax[2].plot(range(0, len_data), data[:,2], color=mflog_utils.tableau20[4])

    ax[0].set_ylabel(u'x μT', fontsize=16)
    ax[1].set_ylabel(u'y μT', fontsize=16)
    ax[2].set_ylabel(u'z μT', fontsize=16)

    ax[0].set_xlim((0, len_data))
    ax[1].set_xlim((0, len_data))
    ax[2].set_xlim((0, len_data))

    ax[0].xaxis.grid(True)
    ax[1].xaxis.grid(True)
    ax[2].xaxis.grid(True)

    ax[2].set_xlabel('Time (s)', fontsize=16)
    ax[2].set_xticks([1524, 3048])
    ax[2].set_xticklabels([30, 60])

    fig.tight_layout()

    dims = ['x', 'y', 'z']
    stds_full = np.std(data, axis=0)
    stds_0030 = np.std(data[:1524,:], axis=0)
    stds_3060 = np.std(data[1524:3048,:], axis=0)
    stds_6090 = np.std(data[3048:,:], axis=0)
    mean_full = np.mean(data, axis=0)
    mean_0030 = np.mean(data[:1524,:], axis=0)
    mean_3060 = np.mean(data[1524:3048,:], axis=0)
    mean_6090 = np.mean(data[3048:,:], axis=0)

    with open(save_name + '.txt', 'w') as f:
        f.write(title + '\n\n')
        f.write('dim,all,-,0-30,-,30-60,-,60-90,-\n')
        
        for i in range(3):
            f.write('{},{},{},{},{},{},{},{},{}\n'.format(
                dims[i],
                mean_full[i], stds_full[i],
                mean_0030[i], stds_0030[i],
                mean_3060[i], stds_3060[i],
                mean_6090[i], stds_6090[i],
            ))

    plt.savefig(save_name + 'png')
    plt.show()

if __name__ == '__main__':
    _, data = mflog_utils.summarise_file('./PeopleTesting/Experiment1.mflog', include_data=True)
    plot_xyz(data, 'People Experiment 1', 'Plots/final/people1')

    _, data = mflog_utils.summarise_file('./PeopleTesting/Experiment2.mflog', include_data=True)
    plot_xyz(data, 'People Experiment 2', 'Plots/final/people2')