import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.ticker import MultipleLocator, NullLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable

import os

path = './data/shuffling_test/'


def triangle_plotter():
    """
    Draw triangles.
    """
    patch1 = []
    patch2 = []

    # get coordinates of triangles
    # loop through each row, from top to bottom, so use reversed range
    for y_corr in reversed(range(10)):
        # loop through each column
        for x_corr in range(10):
            # upper triangle
            index1 = [[x_corr, y_corr], [x_corr + 1, y_corr + 1],
                      [x_corr, y_corr + 1]]
            triangle1 = plt.Polygon(index1)
            patch1.append(triangle1)

            # lower triangle
            index2 = [[x_corr, y_corr], [x_corr + 1, y_corr + 1],
                      [x_corr + 1, y_corr]]
            triangle2 = plt.Polygon(index2)
            patch2.append(triangle2)

    patch1.extend(patch2)

    return patch1


def rectangle_plotter():
    """
    Draw rectangles.
    :return: collection of empty rectangles.
    """
    patch1 = []

    # get coordinates of rectangles
    # loop through each row, from top to bottom, so use reversed range
    for y_corr in reversed(range(10)):
        # loop through each column
        for x_corr in range(10):
            # upper triangle
            rect = Rectangle((x_corr, y_corr), 1, 1)
            patch1.append(rect)

    return patch1


def rectangle_heatmap_plotter(ax, filename, title, last_row):
    """

    :param ax:
    :param filename: filename to read from
    :param title: title of subplot
    :param last_row: boolean. If last_row, plot x-axis labels
    """
    patch1 = rectangle_plotter()

    p = PatchCollection(patch1, cmap='RdYlBu', alpha=0.6)
    p.set_edgecolor('black')

    # map color
    # read color array from file
    file_name = path + filename
    color = np.loadtxt(file_name, delimiter=',')

    p.set_array(np.array(color))
    p.set_clim([1, -12])
    ax.add_collection(p)

    # set y axis
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.set_yticks([t + 0.5 for t in range(10)])
    ylabels = ['{}'.format((i) * 3100 + 100) for i in range(10)]
    ax.set_yticklabels(ylabels, rotation=0, fontsize=10)
    ax.set_ylabel('query extension (bp)')

    # set x axis
    if last_row:
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xticks([t + 0.5 for t in range(10)])
        xlabels = ['{}'.format(i * 3000 + 100) for i in range(10)]
        ax.set_xticklabels(xlabels, rotation=30, fontsize=8)
        ax.set_xlabel('target extension (bp)')
    else:
        ax.xaxis.set_ticks_position('none')

    ax.set_title(title, fontsize=14)
    ax.set_aspect('equal')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    col = plt.colorbar(p, cax=cax)
    col.remove()

    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False

    for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False

#     plt.xlabel('target extension')
#     plt.ylabel('query extension')


def triangle_heatmap_plotter(ax, filename, title, last_row, colorbar, edge):
    """

    :param ax:
    :param filename: filname to read from
    :param title: title of subplot
    :param last_row: boolean. If last_row, plot x-axis labels
    :param colorbar: boolean. Whether to plot colorbar.
    :param edge: boolean. If true, plot black edge.
    """
    patch2 = rectangle_plotter()

    p2 = PatchCollection(patch2, facecolors=(0, 0, 0, 0), edgecolors='black')
    ax.add_collection(p2)

    patch1 = triangle_plotter()

    p = PatchCollection(patch1, cmap='RdYlBu', alpha=0.6)
    if edge:
        p.set_edgecolor('black')

    # map color
    # read color array from file
    file_name = path + filename
    color = np.loadtxt(file_name, delimiter=',')

    p.set_array(np.array(color))
    p.set_clim([1, -12])
    ax.add_collection(p)

    # set y axis
    #     ax.yaxis.set_major_locator(MultipleLocator(1))
    #     ax.set_yticks([t + 0.5 for t in range(10)])
    #     ylabels = ['{}'.format((i) * 3100 + 100) for i in range(10)]
    #     ax.set_yticklabels(ylabels, rotation = 0, fontsize = 10)
    #     ax.set_ylabel('query extension (bp)')

    ax.yaxis.set_ticks_position('none')

    # set x axis
    if last_row:
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xticks([t + 0.5 for t in range(10)])
        xlabels = ['{}'.format(i * 3000 + 100) for i in range(10)]
        ax.set_xticklabels(xlabels, rotation=30, fontsize=8)
        ax.set_xlabel('target extension (bp)')
    else:
        ax.xaxis.set_ticks_position('none')

    ax.set_title(title, fontsize=14)
    ax.set_aspect('equal')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    if colorbar:
        plt.colorbar(p, cax=cax, label='log$_{10}$(q-value)')
    else:
        col = plt.colorbar(p, cax=cax)
        col.remove()

    for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False


def diagonal_heatmap():
    tissue_names = ['limb', 'eye', 'nose', 'forebrain', 'midbrain', 'hindbrain',
                    'heart']

    fig, axes = plt.subplots(7, 3, sharex=True, sharey=True, figsize=(20, 25))

    # plot heatmap by row (one tissue at a time)
    for i in range(len(tissue_names) - 1):
        title1 = tissue_names[i] + ' original'
        title2 = tissue_names[i] + ' total'
        title3 = tissue_names[i] + ' tss'

        file1 = tissue_names[i] + '_original.csv'
        file2 = tissue_names[i] + '_total.csv'
        file3 = tissue_names[i] + '_tss.csv'

        rectangle_heatmap_plotter(axes[i, 0], file1, title1, False)
        triangle_heatmap_plotter(axes[i, 1], file2, title2, False,
                                 False, False)
        triangle_heatmap_plotter(axes[i, 2], file3, title3, False,
                                 False, False)

        # set y axis
        axes[i, 0].yaxis.set_major_locator(MultipleLocator(1))
        axes[i, 0].set_yticks([t + 0.5 for t in range(10)])
        axes[i, 0] = ['{}'.format((j) * 3100 + 100) for j in range(10)]
        # axes[i,0].set_yticklabels(ylabels, rotation = 0, fontsize = 10)
        # axes[i,0].set_ylabel('query extension')

        axes[i, 1].set_xticks([])
        axes[i, 2].set_yticks([])

    # plot last row, include x-axis labels
    rectangle_heatmap_plotter(axes[6, 0], 'heart_original.csv',
                              'heart original', True)
    triangle_heatmap_plotter(axes[6, 1], 'heart_total.csv', 'heart total', True,
                             False, False)
    triangle_heatmap_plotter(axes[6, 2], 'heart_tss.csv', 'heart tss', True,
                             False, False)

    fig.tight_layout(pad=1.0, w_pad=0.8, h_pad=1.2)

    plt.subplots_adjust(bottom=0.15, right=0.5, top=0.9)

    # plot colorbar
    cax = fig.add_axes([0.475, 0.3, 0.015, 0.4])
    cmap = mpl.cm.RdYlBu
    norm = mpl.colors.Normalize(vmin=-12, vmax=1)

    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                    norm=norm, alpha=0.6,
                                    orientation='vertical')
    cb1.set_label('log10(q-value)')
    plt.savefig('shuffling_test.png')


if __name__ == '__main__':
    diagonal_heatmap()
