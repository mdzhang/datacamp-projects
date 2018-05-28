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

df1 = bnames.copy()

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

# drop total_births col used to calculate prop_births
df4 = df3.drop(labels=['total_births'], axis=1)

bnames2 = df4

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
