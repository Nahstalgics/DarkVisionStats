import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from KDEpy import FFTKDE


class Statistics(object):
    def __init__(self, data_frame):
        if not isinstance(data_frame, pd.DataFrame):
            raise TypeError("Statistics must be initialized with a pandas DataFrame.")
        self.data = data_frame.copy()
        self.file_path = None

    def __repr__(self):
        return f"<Statistics file_path={self.file_path!r} rows={len(self.data)}>"

    def setUp(self):
        required_columns = ["depth", "status", "wall_location"]
        missing_cols = [col for col in required_columns if col not in self.data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        self.data = self.data.loc[self.data["wall_location"].notna(), required_columns]

    def plot_histogram(self, column_name, bins):
        if column_name not in self.data.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the data.")

        plt.figure(figsize=(10, 6))
        plt.hist(self.data[column_name].dropna(), bins=bins, edgecolor="black")
        plt.title(f"Histogram of {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        plt.grid(axis="y", alpha=0.75)
        plt.show()

    def create_kde(self):
        if "depth" not in self.data.columns:
            raise ValueError("Cannot create KDE: 'depth' column is missing.")

        depth_series = self.data["depth"].dropna()
        depth_series = depth_series[depth_series > 0]
        if depth_series.empty:
            raise ValueError("Cannot create KDE: no positive 'depth' values to fit.")

        kde = FFTKDE(kernel="gaussian", bw="ISJ").fit(depth_series.values)
        x_grid = np.linspace(depth_series.min(), depth_series.max(), 1000)
        density = kde.evaluate(x_grid)
        return x_grid, density
        
