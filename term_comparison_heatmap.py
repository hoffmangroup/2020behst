import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import gridspec


def create_color_scale():
    heatmap_colors = ["navy", "royalblue", "cornflowerblue", "lightsteelblue",
                      "gainsboro"]
    cmap = LinearSegmentedColormap.from_list("mycmap", heatmap_colors)

    viridis = cm.get_cmap(cmap, 256)
    newcolors = viridis(np.linspace(0, 1, 100000))
    white = np.array([255 / 256, 255 / 256, 255 / 256, 1])
    newcolors[99999:, :] = white
    newcmp = ListedColormap(newcolors)

    return newcmp


def plot_term_heatmap(terms, ground_truth, cmap, title):
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
    ax0 = plt.subplot(gs[0])
    ax0 = sns.heatmap(terms, cmap=cmap, cbar=False)
    ax1 = plt.subplot(gs[1])
    ax1 = sns.heatmap(ground_truth, cmap=cmap, yticklabels=False,
                      cbar_kws={'shrink': 2.0})
    ax1.set_ylabel('')

    fig.tight_layout(pad=1.2)
    plt.savefig(title)


def main():
    limb_all = pd.read_csv('./data/limb_term_comparison.csv')

    # select useful columns and create df for heatmap
    limb_all_heatmap_df = limb_all[
        ['term_name', 'quantile_behst', 'quantile_great',
         'quantile_chip', 'ground_truth']]
    limb_all_heatmap_df.columns = ['GO Term', 'BEHST', 'GREAT', 'ChIP-Enrich',
                                   'Ground Truth']
    limb_all_heatmap_df = limb_all_heatmap_df.set_index('GO Term')

    limb_subplot_all = limb_all_heatmap_df[['BEHST', 'GREAT', 'ChIP-Enrich']]
    limb_subplot_all_ref = limb_all_heatmap_df[['Ground Truth']]

    # select top 50 terms
    limb_subplot_top = limb_all_heatmap_df[
        ['BEHST', 'GREAT', 'ChIP-Enrich']].head(50)
    limb_subplot_top_ref = limb_all_heatmap_df[['Ground Truth']].head(50)

    # create color scale
    cmap = create_color_scale()

    plot_term_heatmap(limb_subplot_all, limb_subplot_all_ref, cmap,
                      "term_comparison_all.png")
    plot_term_heatmap(limb_subplot_top, limb_subplot_top_ref, cmap,
                      'term_comparison_top_50.png')


if __name__ == '__main__':
    main()
