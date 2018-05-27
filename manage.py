import glob
import os
import re

import click
import pandas as pd

BABY_NAME_FILE_REGEX = re.compile('^yob(\d{4}).txt$')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('datapath', type=click.Path(exists=True))
@click.argument('destination')
def baby_names(datapath: str=None, destination: str=None):
    """Generate a datasets/baby_names.csv file from .txt files resulting
    from unzipping the data at https://www.ssa.gov/oact/babynames/names.zip

    :param datapath: absolute path to directory with extracted .txt files
        defaults to ./datasets/baby_names_unzipped/
    :param destination: absolute path to csv to write concatenated data to
        defaults to ./datasets/baby_names.csv

    TODO: fetch zip and unzip as part of this function
    """
    if not datapath:
        datapath = os.path.abspath(
            os.path.join('.', 'datasets', 'baby_names_unzipped'))

    if not destination:
        datapath = os.path.abspath(
            os.path.join('.', 'datasets', 'baby_names.csv'))

    if not datapath or not destination:
        raise ValueError('Missing argument(s)')

    print('Loading data from {}'.format(datapath))
    pattern = os.path.join(datapath, 'yob*.txt')
    files = glob.glob(pattern)

    df_years = []

    for f in files:
        fname = os.path.basename(f)
        matches = BABY_NAME_FILE_REGEX.findall(fname)

        if not matches:
            print('Invalid file name at path: {}'.format(f))
            continue

        year = matches[0]

        df = pd.read_csv(f, header=None, names=['name', 'sex', 'births'])
        df['year'] = year

        df_years.append(df)

    df = pd.concat(df_years)
    df.to_csv(destination, index=False)
    print('Wrote csv to {}'.format(destination))


if __name__ == '__main__':
    cli()
