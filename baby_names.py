import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
    df1 = add_prop_births(bnames)

    mpb = df1.groupby(['sex', 'name'])['prop_births'].max()
    spb = df1.groupby(['sex', 'name'])['prop_births'].sum()

    # convert to dataframe and rename column
    df2 = mpb.to_frame().reset_index()
    df2 = df2.rename(columns={'prop_births': 'max'})

    df3 = spb.to_frame().reset_index()
    df3 = df3.rename(columns={'prop_births': 'total'})

    # create a new dataframe with name/sex/year/births/total_births cols
    df4 = pd.merge(df2, df3, on=['sex', 'name'])

    df4['trendiness'] = df4['max'] / df4['total']

    df4 = pd.merge(df4, df1, on=['sex', 'name'])

    df5 = df4.loc[df4['births'] >= 1000]

    cols = ['sex', 'name', 'max', 'total', 'trendiness']
    df6 = df5.sort_values(['trendiness'], ascending=False)
    df6 = df6.drop_duplicates(subset=['name', 'sex'])
    return df6.reset_index().iloc[0:n][cols]


top10_trendy_names = get_trendy_names(bnames)
