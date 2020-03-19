import utilities as u
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np


class Analyzer:

    data = False
    include_country_regions = []
    exclude_country_regions = []
    include_province_states = []

    def __init__(self, confirmed, death, recovered, include_country_regions=[], exclude_country_regions=[], include_province_states=[]):
        self.include_country_regions = include_country_regions
        self.exclude_country_regions = exclude_country_regions
        self.include_province_states = include_province_states

        datasets_c = [self._clean_data(dataset)
                      for dataset in [confirmed, death, recovered]]

        frame = {
            'confirmed_total': datasets_c[0],
            'death_total': datasets_c[1],
            'recovered_total': datasets_c[2]}

        self.data = pd.DataFrame(frame)

        self.data['current_infected_total'] = self.data['confirmed_total'] - self.data['death_total'] - self.data['recovered_total']

        states = ['confirmed', 'death', 'recovered', 'current_infected']
        self._gen_change_data(states)
        self._gen_change_pct_data(states)
        self._gen_change_pct_avg_data(states)

        # self.data['confirmed_change%3a']

        self.data['lethality'] = self.data['death_total'] / self.data['recovered_total']

    def _gen_change_data(self, states):
        for state in states:
            self.data[state+'_change'] = self.data[state+'_total'].diff()

    def _gen_change_pct_data(self, states):
        for state in states:
            self.data[state+'_change%'] = self.data[state+'_total'].pct_change()

    def _gen_change_pct_avg_data(self, states):
        for state in states:
            self.data[state+'_change%3a'] = self.data[state+'_change%'].rolling(window=4, min_periods=0).mean()

    def _clean_data(self, data):
        for country_region in self.exclude_country_regions:
            data = data[data['Country/Region'] != country_region]

        if len(self.include_country_regions) > 0:
            data = data[np.isin(data['Country/Region'], self.include_country_regions)]

        # TODO include_province_states filter

        data = data.drop(columns=['Province/State', 'Country/Region', 'Lat', 'Long'])
        data = data.aggregate('sum')
        data.index.name = 'date'
        data.index = pd.to_datetime(data.index)
        return data

    def get_dataframe(self):
        return self.data

    def graph_data(self, columns=[], since_x_days_ago=0, upto_x_days_ago=0):
        if len(columns) == 0:
            self.graph_totals(since_x_days_ago, upto_x_days_ago)
        else:
            for column in columns:
                plt.plot(self.data[column][-since_x_days_ago:len(self.data[column]) - upto_x_days_ago], label=column)
            plt.gcf().autofmt_xdate()
            plt.show()

    def graph_totals(self, since_x_days_ago=0, upto_x_days_ago=0):
        self.graph_append('_total', since_x_days_ago, upto_x_days_ago)

    def graph_changes(self, since_x_days_ago=0, upto_x_days_ago=0):
        self.graph_append('_change', since_x_days_ago, upto_x_days_ago)

    def graph_changes_pct(self, since_x_days_ago=0, upto_x_days_ago=0):
        self.graph_append('_change%', since_x_days_ago, upto_x_days_ago)

    def graph_changes_pct_avg(self, since_x_days_ago=0, upto_x_days_ago=0):
        self.graph_append('_change%3a', since_x_days_ago, upto_x_days_ago)

    def graph_append(self, append='', since_x_days_ago=0, upto_x_days_ago=0):
        since_x_days_ago = -since_x_days_ago
        upto_x_days_ago = len(self.data) - upto_x_days_ago
        plt.plot(self.data['death'+append][since_x_days_ago:upto_x_days_ago], color='red', label='death')
        plt.plot(self.data['current_infected'+append][since_x_days_ago:upto_x_days_ago], color='purple', label='current infected')
        plt.plot(self.data['confirmed'+append][since_x_days_ago:upto_x_days_ago], color='orange', linestyle='dashed', label='confirmed total')
        plt.plot(self.data['recovered'+append][since_x_days_ago:upto_x_days_ago], color='green', label='recovered')
        plt.gcf().autofmt_xdate()
        plt.show()


class DataDownloader:

    confirmed = False
    death = False
    recovered = False

    def __init__(self):
        if not (self.confirmed or self.death or self.recovered):
            self.confirmed, self.death, self.recovered = u.fetch_virus_data()

    def get_analyzer(self, include_country_regions=[], exclude_country_regions=[], include_province_states=[]):
        return Analyzer(
            self.confirmed,
            self.death,
            self.recovered,
            include_country_regions,
            exclude_country_regions,
            include_province_states
        )

    def display_countries(self):
        pd.options.display.max_rows = 1000
        displayed = []
        for country in self.confirmed['Country/Region']:
            if country not in displayed:
                print(country)
                displayed.append(country)

    def display_locations(self):
        pd.options.display.max_rows = 1000
        print(self.confirmed['Province/State', 'Country/Region'])

