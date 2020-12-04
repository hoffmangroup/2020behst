import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_precision_recall(data, title):
    sns.set(font_scale=1.2)
    sns.set_style("darkgrid")
    g = sns.relplot(x="recall", y="precision", hue="label",  col='tissue',
                    size='terms', col_wrap=3, data=data,
                    alpha=1, sizes=(30, 500), palette='colorblind')

    # plt.legend(loc='lower right')
    leg = g._legend
    leg.set_bbox_to_anchor([0.75,0.25])

    # plt.show()
    plt.savefig(title)


if __name__ == '__main__':
    data_bp_mf = pd.read_csv("./data/precision_recall_data.csv")
    data_bp = pd.read_csv("./data/precision_recall_data_bp.csv")

    # edit subtitle
    # nGT = number of Ground Truth terms
    # nTP = number of True Positive terms
    # nFP = number of False Positive terms
    plot_df = data_bp_mf.replace({'limb': 'limb (nGT=175, nTP=54, nFP=1)',
                                  'forebrain': 'forebrain (nGT=256, nTP=33, nFP=0)',
                                  'midbrain': 'midbrain (nGT=98, nTP=26, nFP=7)',
                                  'hindbrain': 'hindbrain (nGT=9, nTP=7, nFP=69)',
                                  'heart': 'heart (nGT=344, nTP=0, nFP=3)'})

    plot_df_bp = data_bp.replace({'limb': 'limb (nGT=157, nTP=38, nFP=0)',
                                  'forebrain': 'forebrain (nGT=229, nTP=16, nFP=0)',
                                  'midbrain': 'midbrain (nGT=76, nTP=9, nFP=7)',
                                  'hindbrain': 'hindbrain (nGT=2, nTP=0, nFP=58)',
                                  'heart': 'heart (nGT=312, nTP=0, nFP=3)'})

    plot_precision_recall(plot_df, 'precision_recall_bp_mf.png')
    plot_precision_recall(plot_df_bp, 'precision_recall_bp_only.png')
