"""
ADCP Data Processor
Processes current speed and direction data from ADCP.
"""

import numpy as np
import pandas as pd
from datetime import datetime
from scipy import signal


class ADCPProcessor:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = None

    def load_data(self):
        """Load ADCP data."""
        self.data = pd.read_csv(self.data_file)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        return self.data

    def calculate_current_statistics(self):
        """Calculate current speed and direction statistics."""
        self.data['speed'] = np.sqrt(
            self.data['u_component']**2 + self.data['v_component']**2
        )

        self.data['direction'] = np.degrees(
            np.arctan2(self.data['v_component'], self.data['u_component'])
        )
        self.data['direction'] = (self.data['direction'] + 360) % 360

        stats = {
            'speed': {
                'mean': self.data['speed'].mean(),
                'std': self.data['speed'].std(),
                'max': self.data['speed'].max(),
            },
            'direction': {
                'mean': self.data['direction'].mean(),
                'std': self.data['direction'].std(),
            },
        }
        return stats

    def extract_tidal_signal(self):
        """Extract tidal signal from current data."""
        detrended = signal.detrend(self.data['speed'])

        sos = signal.butter(4, 0.1, 'low', fs=1/600, output='sos')
        tidal = signal.sosfilt(sos, detrended)

        return tidal

    def validate_against_tidal_charts(self, tidal_charts_file):
        """Validate ADCP data against tidal elevation charts."""
        tidal_charts = pd.read_csv(tidal_charts_file)
        tidal_charts['timestamp'] = pd.to_datetime(tidal_charts['timestamp'])

        merged = pd.merge_asof(
            self.data.sort_values('timestamp'),
            tidal_charts.sort_values('timestamp'),
            on='timestamp',
            direction='nearest'
        )

        correlation = merged['speed'].corr(merged['tidal_elevation'])
        rmse = np.sqrt(np.mean((merged['speed'] - merged['tidal_elevation'])**2))

        return {
            'correlation': correlation,
            'rmse': rmse
        }
