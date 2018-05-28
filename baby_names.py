import matplotlib.pyplot as plt
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
    def build_result_df(grp, total_births, max_births, trendiness):
        name = grp['name'].reset_index(drop=True)[0]
        sex = grp['sex'].reset_index(drop=True)[0]

        result = pd.DataFrame(
            {
                'name': name,
                'sex': sex,
                'total': total_births,
                'max': max_births,
                'trendiness': trendiness,
            },
            index=[[name], [sex]])
        result.index.set_names(['name', 'sex'], inplace=True)

        return result

    def birth_metrics(grp):
        total_births = grp['births'].sum()
        prop_births = grp['births'] / total_births

        mpb = prop_births.max()
        spb = prop_births.sum()

        trendiness = mpb / spb

        mb = grp['births'].max()

        return build_result_df(grp, total_births, mb, trendiness)

    df1 = df.set_index(['name', 'sex'])
    too_few = df1[df1['births'] <= 1000]
    df2 = df1[~df1.index.isin(too_few.index)]

    df3 = df2.reset_index().groupby(['sex', 'name']).apply(birth_metrics)
    df4 = df3.reset_index(drop=True)

    df5 = df4.sort_values(['trendiness'], ascending=False)
    return df5.head(n).reset_index()


top10_trendy_names = get_trendy_names(bnames)
