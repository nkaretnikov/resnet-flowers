#!/usr/bin/env python3

# Pull images from the dataset and label them.

import pandas as pd
import subprocess as sp
import sys

DATA_DIR = sys.argv[1]  # flower_images
OUT_DIR = sys.argv[2]  # ../images
LABELS = 'flower_labels.csv'

LABEL_MAP = {
    0: 'phlox',
    1: 'rose',
    2: 'calendula',
    3: 'iris',
    4: 'leucanthemum maximum',
    5: 'bellflower',
    6: 'viola',
    7: 'rudbeckia laciniata',
    8: 'peony',
    9: 'aquilegia'
}

df = pd.read_csv(f'{DATA_DIR}/{LABELS}')
df.replace(to_replace=LABEL_MAP, inplace=True)  # use labels instead of numbers

# Print the first N values in each group.
df = df[df.file != '0038.png']  # skip undesired values
res = df.groupby('label').head(1).sort_values('label')

sp.run(['mkdir', '-p', f'{OUT_DIR}'])

for ix, row in res.iterrows():
    src = '{}/{}'.format(DATA_DIR, row['file'])
    label = '-'.join(row['label'].split(' '))
    tgt = '{}/{}.png'.format(OUT_DIR, label)
    sp.run(['cp', src, tgt])
