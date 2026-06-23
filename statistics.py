import numpy as np
import scipy as sp
import pandas as pd
import statsmodels as sm
import matplotlib.pyplot as plt
import altair as alt
from sklearn.neighbors import KernelDensity

class Statistics(object):
    ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

    def __init__(self, file_path):
        file_path = str(file_path)
        extension = file_path.lower().rsplit('.', 1)[-1] if '.' in file_path else ''
        extension = f".{extension}"
        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError("Only .csv or .xlsx files are supported.")

        if extension == ".csv":
            self.data = pd.read_csv(file_path)
        else:
            self.data = pd.read_excel(file_path)

        self.file_path = file_path

    def __repr__(self):
        return f"<Statistics file_path={self.file_path!r} rows={len(self.data)}>"
    
    def setUp(self):
        self.data.loc[self.data["depth"],"depth":"wall_location"]

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
        observations = len(self.data)

        silverman_bandwidth = 1.06 * standard_deviation * observations**(-1/5)  
        kde = KernelDensity(kernel='gaussian', bandwidth=silverman_bandwidth).fit(self.data.values.reshape(-1, 1))
        x_d = np.linspace(self.data.min(), self.data.max(), 1000)
        return kde

        
        
