from itertools import chain

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.core.debugger import Pdb

sns.set()

#######################################################################
# read in data
#######################################################################

bnames = pd.read_csv('datasets/baby_names.csv')
bnames.head()

#######################################################################
# Get the top 5 most popular male & top 5 most popular female baby names
# of babies born 2011 and later
#######################################################################

cols = ['sex', 'name', 'births']
df1 = bnames[bnames.year >= 2011][cols]

# collapse duplicate rows (for each year since 2011) by summing births
births = df1.groupby(['name', 'sex'])['births'].sum()

df2 = births.to_frame().reset_index()
df3 = df2.groupby(['sex']).apply(lambda g: g.nlargest(5, columns=['births']))

# drop 'sex' group by index
df4 = df3.reset_index(drop=True)

bnames_top5 = df4

#######################################################################
# compute the proportion of births by year and add it as a new column
# prop_births
#######################################################################


def add_prop_births(df):
    df1 = df.copy()

    # get a series with year index and births column holding
    # total births by year
    total_births = df1.groupby(['year'])['births'].sum()

    # convert to dataframe and rename births column total_births
    df2 = total_births.to_frame().reset_index()
    df2 = df2.rename(columns={'births': 'total_births'})

    # create a new dataframe with name/sex/year/births/total_births cols
    df3 = pd.merge(df1, df2, on='year')
    # calculate proportion births in new col
    df3['prop_births'] = df3.births / df3.total_births

    return df3.drop(labels=['total_births'], axis=1)


bnames2 = add_prop_births(bnames)

#######################################################################
# plot popularity of the female names Elizabeth and Deneen
#######################################################################


def plot_names(name, sex):
    data = bnames.loc[(bnames['name'] == name) & (bnames['sex'] == sex)]
    plt.plot(data['year'], data['births'])
    plt.xlabel('Year')
    plt.ylabel('Number of births')

    # add graph title
    gender = {'F': 'female', 'M': 'male'}[sex]

    plt.title('Number births per year of {} babies named {}'.format(gender,
                                                                    name))
    plt.show()


plot_names('Elizabeth', 'F')
plot_names('Deneen', 'F')

num_peaks_elizabeth = 3
num_peaks_deneen = 1

#######################################################################
# find the top 10 trendy names with at least a 1000 births
# where trendiness = max proportion / sum(proportions across all years)
#######################################################################


def get_trendy_names(df, n=10):
    df2 = df

    df3 = df2.groupby(['sex', 'name'])['births'].agg({
        'max': np.max,
        'total': np.sum,
    })
    df3['trendiness'] = df3['max'] / df3['total']
    df4 = df3.reset_index(drop=False)
    df5 = df4[df4['total'] > 1000]

    df6 = df5.sort_values(['trendiness'], ascending=False)
    return df6.head(n).reset_index(drop=True)


top10_trendy_names = get_trendy_names(bnames)

#######################################################################
# How many people born in Year X are still alive in 2016?
#######################################################################

lifetables = pd.read_csv('datasets/lifetables.csv')

lt = lifetables
df1 = lt[lt['year'] + lt['age'] == 2016]

lifetables_2016 = df1

# lx = # people born in a year who live upto a given age
plt.plot(df1['year'], df1['lx'])
plt.xlabel('Year')
plt.ylabel('Life expectancy')
plt.title('Life expectancy by year of birth')
plt.show()

#######################################################################
# Same as above, but smoothen curve by using linear inteperpolation
# to fill in missing years
# Limit to 1900-2015
#######################################################################

df1 = lt[(lt['year'] + lt['age'] == 2016) & (lt['year'].isin(
    range(1900, 2016)))]
df2 = df1[['sex', 'year', 'lx']]

years = [y for y in range(1900, 2016) if y % 10 != 0]
missing = list(
    chain(zip(years, 'M' * len(years)), zip(years, 'F' * len(years))))

df3 = pd.DataFrame(missing, columns=['year', 'sex'])
df3['lx'] = np.nan

df4 = pd.concat([df2, df3]).reset_index(drop=True).sort_values('year')
df4['lx'] = df4['lx'].interpolate()
df4 = df4.sort_values(['sex', 'year'])

lifetable_2016_s = df4

#######################################################################
# Plot year (x-axis) against # births (y-axis) for
# boys named Joseph, girls named Brittany
# plot total # births as a line
# fill # people still alive under that line, in a different color
#######################################################################


def get_data(name, sex):
    df0 = bnames[(bnames['name'] == name) & (bnames['sex'] == sex)]
    df1 = lifetable_2016_s[lifetable_2016_s['sex'] == sex]
    df2 = pd.merge(df0, df1, on=['sex', 'year'])
    df2['n_alive'] = (df2['lx'] * df2['births']) / 100000
    return df2[['name', 'sex', 'births', 'lx', 'n_alive', 'year']]


def plot_data(name, sex):
    df = get_data(name, sex)
    df2 = df[['year', 'births', 'n_alive']]
    gender = {'F': 'females', 'M': 'males'}[sex]

    ax = df2.plot.line(x='year', y='births')
    df2.plot(kind='area', x='year', y='n_alive', ax=ax)
    plt.xlabel('Year')
    plt.ylabel('Number of births')
    plt.title('Births and No births still alive by year for {} named {}'
              .format(gender, name))
    plt.show()


plot_data('Joseph', 'M')
plot_data('Brittany', 'F')
