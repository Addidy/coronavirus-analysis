import os.path
from git import Repo
import pandas as pd


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
    # return dataframe
    confirmed = pd.read_csv('./datasets/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
    deaths    = pd.read_csv('./datasets/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
    recovered = pd.read_csv('./datasets/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
    return confirmed, deaths, recovered
