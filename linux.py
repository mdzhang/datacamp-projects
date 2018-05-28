import datetime
from itertools import chain

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.core.debugger import Pdb
from wquantiles import quantile

sns.set()

#######################################################################
# Print the content of git_log_excerpt.csv
#######################################################################

with open('datasets/git_log_excerpt.csv', 'r') as f:
    print(f.read())

#######################################################################
# read data from full file
#######################################################################

df = pd.read_csv(
    'datasets/git_log.gz',
    compression='gzip',
    sep='#',
    encoding='latin-1',
    header=None,
    names=['timestamp', 'author'])
git_log = df
git_log.head()

#######################################################################
# pull basic metrics
#######################################################################

nc = git_log.shape[0]
number_of_commits = nc

na = git_log['author'].nunique()
number_of_authors = na

print("%s authors committed %s code changes." %
      (number_of_authors, number_of_commits))

#######################################################################
# get the top 10 contributors
#######################################################################

s1 = git_log.groupby('author')['timestamp'].count()
s2 = s1.sort_values(ascending=False).head(10)
top_10_authors = s2

#######################################################################
# convert timestamp column
#######################################################################

df1 = df.copy()
df1['timestamp'] = pd.to_datetime(df['timestamp'], errors='ignore', unit='s')
df1 = df1.sort_values('timestamp')
git_log = df1
git_log.describe()

#######################################################################
# drop bad timestamps
#######################################################################

df1 = df.copy()
df1['timestamp'] = pd.to_datetime(df['timestamp'], errors='ignore', unit='s')
df2 = df1.set_index('timestamp').sort_index()

ts = df2[df2['author'] == 'Linus Torvalds'].take([0]).index.values[0]
first_commit_timestamp = pd.to_datetime(ts)
last_commit_timestamp = pd.to_datetime(datetime.datetime.now())

df3 = df2[str(first_commit_timestamp):str(last_commit_timestamp)]

corrected_log = df3
corrected_log['timestamp'].describe()
