#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.ticker import MultipleLocator, NullLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker

import os


def read_pvalue(filename):
    df = pd.read_csv(filename, sep=' ', header=None)
    df.columns = ['p_value', 'Query extension', 'Target extension']
    df["log10_p_value"] = np.log10(df.p_value)
    df = df.sort_values(by=['Query extension', 'Target extension'])
    df = df.drop_duplicates()
    # reshape dataframe for heatmap
    heatmap_df = df.pivot("Query extension", "Target extension", "log10_p_value")
    
    return heatmap_df

# read data
limb_df = read_pvalue('./data/extension_parameter/vista_LIMB_sorted_lowest_pvalue_oneside_selected_col.txt')
eye_df = read_pvalue('./data/extension_parameter/vista_EYE_sorted_lowest_pvalue_oneside_selected_col.txt')
forebrain_df = read_pvalue('./data/extension_parameter/vista_FOREBRAIN_sorted_lowest_pvalue_oneside_selected_col.txt')
midbrain_df = read_pvalue('./data/extension_parameter/vista_MIDBRAIN_sorted_lowest_pvalue_oneside_selected_col.txt')
hindbrain_df = read_pvalue('./data/extension_parameter/vista_HINDBRAIN_sorted_lowest_pvalue_oneside_selected_col.txt')
nose_df = read_pvalue('./data/extension_parameter/vista_NOSE_sorted_lowest_pvalue_oneside_selected_col.txt')
heart_df = read_pvalue('./data/extension_parameter/vista_HEART_sorted_lowest_pvalue_oneside_selected_col.txt')

# calculate average of the seven dataframes
avg_df = (limb_df + eye_df + forebrain_df + midbrain_df + hindbrain_df + nose_df + heart_df) / 7

# find query and target extensions that return the most negative average q-value
a, b = avg_df.stack().idxmin()
print(avg_df.loc[[a], [b]])


def rectangle_plotter():
    """
    Plot rectangle grids for heatmap.
    """
    patch1 = []

    # get coordinates of rectangles
    # loop through each row, from top to bottom, so use reversed range
    for y_corr in reversed(range(11)):
        # loop through each column
        for x_corr in range(11):
            # upper triangle
            rect = Rectangle((x_corr,y_corr),1,1)
            patch1.append(rect) 
    
    return patch1


def fmt(x, pos):
    """
    Format number with scientific notation.
    """
    return r'$10^{{{}}}$'.format(x)


def rectangle_heatmap_plotter(ax, df, title, last_row, colorbar):
    """
    Plot heatmap and colorbar.
    """
    # plot grid
    patch1 = rectangle_plotter()   

    p = PatchCollection(patch1, cmap='RdYlBu', alpha=0.6)
    p.set_edgecolor('black')
    # map color
    color = df.values.flatten()
    p.set_array(np.array(color))
    # p.set_clim([1, -12])

    ax.add_collection(p)
    
    # set y axis
    ax.yaxis.set_major_locator(MultipleLocator(1))    
    ax.set_yticks([t + 0.5 for t in range(11)])
    ylabels = ['{}'.format((i) * 1600 + 1000) for i in reversed(range(11))]
    ax.set_yticklabels(ylabels, rotation = 0, fontsize = 10)
    ax.set_ylabel('Query extension (bp)')
    
    # set x axis
    if last_row:
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xticks([t + 0.5 for t in range(11)])
        xlabels = ['{}'.format(i * 1500 + 1000) for i in range(11)]
        ax.set_xticklabels(xlabels, rotation = 30, fontsize = 8)
        ax.set_xlabel('Target extension (bp)')
    else:
        ax.xaxis.set_ticks_position('none') 
    
    ax.set_title(title,fontsize = 10)
    ax.set_aspect('equal')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 11)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)

    # plot colorbar
    col = plt.colorbar(p, cax = cax, format=ticker.FuncFormatter(fmt))
    col.ax.set_ylabel("Geometric mean of q-value")
    
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False

    for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        
    # draw selected square in green
    ax.add_patch(Rectangle((5, 4), 1, 1, fill=False, edgecolor='lawngreen', lw=3))
    plt.savefig('./extension_parameters.png', dpi=150, bbox_inches="tight")

# plot figure
fig, ax = plt.subplots()
rectangle_heatmap_plotter(ax, avg_df, '', True, True)