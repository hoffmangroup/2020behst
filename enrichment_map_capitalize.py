#!/usr/bin/python

import sys
import pandas as pd

filename = sys.argv[1]
result = sys.argv[2]

print("Capitalize column in file:", filename)

df = pd.read_csv(filename)
df['EnrichmentMap::GS_DESCR_Capitalize'] = df['EnrichmentMap::GS_DESCR'].str.capitalize()
df = df.replace({'EnrichmentMap::GS_DESCR_Capitalize': {'Dna': 'DNA', 'dna': 'DNA', 'Rna': 'RNA', 'rna': 'RNA', 'C-c': 'C-C', 'c-c': 'C-C'}})

print("File written to:", result)
df[['EnrichmentMap::Name', 'EnrichmentMap::GS_DESCR_Capitalize']].to_csv(result, index=None)
