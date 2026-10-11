"""
MIKE 21 Extract Results
Extract results from MIKE 21 FM output.
"""

import numpy as np
import pandas as pd
from pathlib import Path


class MIKE21ResultsExtractor:
    def __init__(self, output_dir='mike21_results'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_currents(self, result_file):
        """Extract current speed and direction from result file."""
        try:
            import mikeio
            dfs = mikeio.dfs2.Dfs2(result_file)
            data = dfs.read()

            u = data['U'].values
            v = data['V'].values

            speed = np.sqrt(u ** 2 + v ** 2)
            direction = np.degrees(np.arctan2(v, u))
            direction = (direction + 360) % 360

            return {
                'speed': speed,
                'direction': direction,
                'u': u,
                'v': v,
            }
        except ImportError:
            print("mikeio not installed. Using placeholder.")
            return None

    def save_to_netcdf(self, data, output_file='currents.nc'):
        """Save extracted data to NetCDF."""
        import xarray as xr

        ds = xr.Dataset(
            {
                'speed': (['time', 'lat', 'lon'], data['speed']),
                'direction': (['time', 'lat', 'lon'], data['direction']),
                'u': (['time', 'lat', 'lon'], data['u']),
                'v': (['time', 'lat', 'lon'], data['v']),
            }
        )

        output_path = self.output_dir / output_file
        ds.to_netcdf(output_path)
        print(f"Results saved to {output_path}")

        return output_path


if __name__ == "__main__":
    extractor = MIKE21ResultsExtractor()
    # extractor.extract_currents('results.dfs2')
