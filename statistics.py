import os
import numpy as np
import scipy as sp
import pandas as pd
import statsmodels as sm
import matplotlib.pyplot as plt
import altair as alt
from sklearn.neighbors import KernelDensity

class Statistics(object):
    def __init__(self, data_frame):
        if not isinstance(data_frame, pd.DataFrame):
            raise TypeError("Statistics must be initialized with a pandas DataFrame.")
        self.data = data_frame
        self.file_path = None

    def __repr__(self):
        return f"<Statistics file_path={self.file_path!r} rows={len(self.data)}>"
    
    def setUp(self):
        self.data.loc[self.data["wall_location"] != np.nan, "depth":"wall_location"]

    def plot_histogram(self, column_name, bins):
        if column_name not in self.data.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the data.")

        plt.figure(figsize=(10, 6))
        plt.hist(self.data[column_name].dropna(), bins=bins, edgecolor='black')
        plt.title(f'Histogram of {column_name}')
        plt.xlabel(column_name)
        plt.ylabel('Frequency')
        plt.grid(axis='y', alpha=0.75)
        plt.show()

    def create_kde(self):

    
        standard_deviation = self.data.std()
        total_observations = len(self.data)
        approved_data = self.data[self.data["depth"] > 0]
        approved_observations = len(approved_data)



        silverman_bandwidth = 1.06 * standard_deviation * observations**(-1/5)
        # sheather_jones   
        kde = KernelDensity(kernel='gaussian', bandwidth=silverman_bandwidth).fit(self.data.values.reshape(-1, 1))
        x_d = np.linspace(self.data.min(), self.data.max() , 1000)
        return kde

        
        
