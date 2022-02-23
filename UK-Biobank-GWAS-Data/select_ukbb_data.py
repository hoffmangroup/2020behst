#!/usr/bin/env python3.5

import sys
import pandas as pd

def process_df(filename, result):
    print('read data from:', filename)
    df = pd.read_csv(filename, sep=' ', header=0)
    print('length of input:', len(df))
    df_sig = df[df.pval_meta <= 0.00000001]
    print('length of significant terms:', len(df_sig))

    df_sig['chrom'] = 'chr' + df_sig['chr'].astype(str)

    # change from 1-coordinate to 0-coordinate
    # add 1k bp extension on both sides to get 2k bp region
    df_sig['start'] = df_sig['pos'] - 1 - 1000
    df_sig['end'] = df_sig['pos'] - 1 + 1000

    print('output saved to:', result)
    df_sig[['chrom','start','end']].to_csv(result, header=None, index=None, sep='\t')

process_df(sys.argv[1], sys.argv[2])
