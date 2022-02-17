import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.ticker import MultipleLocator, NullLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker

import os

path = './data/shuffling_test_2022/'

def fmt(x, pos):
    """
    Format number with scientific notation.
    """
    cut_off = -5
    if x > cut_off:
      return "{:.5f}".format(pow(10,x)).rstrip('0').rstrip('.')
    else:
      return r'$10^{{{}}}$'.format(format(x).rstrip('0').rstrip('.'))

def triangle_plotter():
    """
    Draw triangles.
    """
    patch1 = []
    patch2 = []

    # get coordinates of triangles
    # loop through each row, from top to bottom, so use reversed range
    for y_corr in reversed(range(11)):
        # loop through each column
        for x_corr in range(11):
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
    for y_corr in reversed(range(11)):
        # loop through each column
        for x_corr in range(11):
            # upper triangle
            rect = Rectangle((x_corr, y_corr), 1, 1)
            patch1.append(rect)

    return patch1

def rectangle_heatmap_plotter(ax, filename, title, last_row, first_col):
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
    p.set_clim([0, -10])
    ax.add_collection(p)

    # set y axis
    if first_col:
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.set_yticks([t + 0.5 for t in range(11)])
        ylabels = ['{}'.format((i) * 1600 + 1000) for i in range(11)]
        ax.set_yticklabels(ylabels, rotation=0, fontsize=12)
        ax.set_ylabel('query extension (bp)', fontsize=16)
    else:
        ax.set_yticks([])

    # set x axis
    if last_row:
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xticks([t + 0.5 for t in range(11)])
        xlabels = ['{}'.format(i * 1500 + 1000) for i in range(11)]
        ax.set_xticklabels(xlabels, rotation=60, fontsize=12)
        ax.set_xlabel('target extension (bp)', fontsize=16)
    else:
        ax.set_xticks([])


    ax.set_title(title, fontsize=16)
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
    p.set_clim([0, -10])
    ax.add_collection(p)

    ax.set_yticks([])

    # set x axis
    if last_row:
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xticks([t + 0.5 for t in range(11)])
        xlabels = ['{}'.format(i * 1500 + 1000) for i in range(11)]
        ax.set_xticklabels(xlabels, rotation=60, fontsize=12)
        ax.set_xlabel('target extension (bp)', fontsize=16)
    else:
        ax.set_xticks([])

    ax.set_title(title, fontsize=16)
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
    fig, axes = plt.subplots(4, 6, figsize=(20,16))

#    fig, axes = plt.subplots(4, 6, sharex=True, sharey=True, figsize=(20,16))
    axes[3,3].axis('off')
    axes[3,4].axis('off')
    axes[3,5].axis('off')

    # plot heatmap by row (one tissue at a time)
    for i in range(len(tissue_names)):
        title1 = tissue_names[i] + ' original'
        title2 = tissue_names[i] + ' total'
        title3 = tissue_names[i] + ' tss'

        file1 = tissue_names[i] + '_original.csv'
        file2 = tissue_names[i] + '_total.csv'
        file3 = tissue_names[i] + '_tss.csv'

        i_ax = i if i < 4 else i - 4
        j_ax_shift = 0 if i < 4 else 3
        
        plot_xlabel = True if i == 3 or i == 6 else False
        plot_ylabel = True if i < 4 else False
        rectangle_heatmap_plotter(axes[i_ax, 0 + j_ax_shift], file1, title1, plot_xlabel, plot_ylabel)
        triangle_heatmap_plotter(axes[i_ax, 1 + j_ax_shift], file2, title2, plot_xlabel,
                                 False, False)
        triangle_heatmap_plotter(axes[i_ax, 2 + j_ax_shift], file3, title3, plot_xlabel,
                                 False, False)
        # Add highlight rectangle
        for j in range(3):
            axes[i_ax, j + j_ax_shift].add_patch(Rectangle((5,6), 1, 1, fill=False, edgecolor='lawngreen', lw=3))

        #axes[i_ax, 1 + j_ax_shift].set_xticks([])
        #axes[i_ax, 2 + j_ax_shift].set_yticks([])

    fig.tight_layout(pad=1.0, w_pad=0.8, h_pad=1.2)
    plt.subplots_adjust(bottom=0.15, right=0.9, top=0.9)

    # plot triangle icons    
    axes[3,3].axis([0,1,0,1])
    icon_patch = [plt.Polygon([[0.02, 0.22],[0.22, 0.22],[0.02, 0.02]]), plt.Polygon([[0.02, 0.02],[.22, .22],[.22, 0.02]])]
    p = PatchCollection(icon_patch, cmap='RdYlBu', alpha=0.6)
    p.set_edgecolor('white')
    p.set_array([-2, -6])
    p.set_clim([-10, 0])
    axes[3,3].add_collection(p)

    axes[3,3].plot([0.02, 0.02, 0.22, 0.22, 0.02], [0.02, 0.22, 0.22, 0.02, 0.02], 'k')
    axes[3,3].text(0.01, 0.24, "75%", fontsize = 12)
    axes[3,3].text(0.08, -0.06, "25%", fontsize = 12)   
 
    # plot colorbar
    cax = fig.add_axes([0.48, 0.24, 0.4, 0.012])
    cmap = mpl.cm.RdYlBu
    norm = mpl.colors.Normalize(vmin=-10, vmax=0)

    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                    norm=norm, alpha=0.6,
                                    orientation='horizontal',
                                    format=ticker.FuncFormatter(fmt))
    cb1.ax.tick_params(labelsize=14)
    cb1.set_label('q-value', size = 16, labelpad=-60)
    plt.savefig('shuffling_test.png', bbox_inches="tight")



if __name__ == '__main__':
    diagonal_heatmap()
