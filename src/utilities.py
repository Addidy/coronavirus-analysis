import os.path
from git import Repo
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import matplotlib.pyplot as plt


def fetch_virus_data():
    # Check if there is data.
    if os.path.isdir('./datasets/archived_data'):
        print('Getting latest data...')
        repo = Repo('./datasets')
        git = repo.git
        pull_msg_result = git.pull('origin', 'master')
        print(pull_msg_result)
    else:
        print('No Data found.\nPerforming first time setup...\nDownloading Data... (This can take a minute)')
        Repo.clone_from("https://github.com/CSSEGISandData/COVID-19.git", "./datasets")
        print('Setup Complete.')
    confirmed = pd.read_csv('./datasets/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    deaths    = pd.read_csv('./datasets/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    recovered = pd.read_csv('./datasets/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    return confirmed, deaths, recovered


def graph_financial_data(ticker):
    start = dt.datetime(2020, 1, 20)
    end = dt.datetime.now()

    df = web.DataReader(ticker, 'yahoo', start, end)
    df['Adj Close'].plot()
    #return df
