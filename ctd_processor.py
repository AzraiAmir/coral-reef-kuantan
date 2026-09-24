"""
Physicochemical Data Processor
Processes temperature, salinity, pH, turbidity, and dissolved oxygen data.
"""

import pandas as pd
import numpy as np
from datetime import datetime


class PhysicochemicalProcessor:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = None

    def load_data(self):
        """Load physicochemical data from CSV."""
        self.data = pd.read_csv(self.data_file)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        return self.data

    def calculate_statistics(self):
        """Calculate descriptive statistics."""
        stats = {
            'temperature': {
                'mean': self.data['temperature_c'].mean(),
                'std': self.data['temperature_c'].std(),
                'min': self.data['temperature_c'].min(),
                'max': self.data['temperature_c'].max(),
            },
            'salinity': {
                'mean': self.data['salinity_psu'].mean(),
                'std': self.data['salinity_psu'].std(),
                'min': self.data['salinity_psu'].min(),
                'max': self.data['salinity_psu'].max(),
            },
            'ph': {
                'mean': self.data['ph'].mean(),
                'std': self.data['ph'].std(),
                'min': self.data['ph'].min(),
                'max': self.data['ph'].max(),
            },
            'turbidity': {
                'mean': self.data['turbidity_ntu'].mean(),
                'std': self.data['turbidity_ntu'].std(),
                'min': self.data['turbidity_ntu'].min(),
                'max': self.data['turbidity_ntu'].max(),
            },
            'dissolved_oxygen': {
                'mean': self.data['do_mgl'].mean(),
                'std': self.data['do_mgl'].std(),
                'min': self.data['do_mgl'].min(),
                'max': self.data['do_mgl'].max(),
            },
        }
        return stats

    def detect_thermal_anomalies(self, threshold=1.0):
        """Detect thermal anomalies (potential bleaching events)."""
        mean_temp = self.data['temperature_c'].mean()
        std_temp = self.data['temperature_c'].std()

        anomalies = self.data[
            self.data['temperature_c'] > mean_temp + threshold * std_temp
        ]

        return anomalies

    def calculate_turbidity_index(self):
        """Calculate turbidity index for each site."""
        turbidity_by_site = self.data.groupby('site_id')['turbidity_ntu'].mean()
        return turbidity_by_site


if __name__ == "__main__":
    processor = PhysicochemicalProcessor("data/physicochemical_data.csv")
    processor.load_data()
    stats = processor.calculate_statistics()
    print(stats)
