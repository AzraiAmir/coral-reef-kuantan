"""
Habitat Mapping
Generates continuous habitat maps from detection outputs.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from scipy.interpolate import griddata


class HabitatMapper:
    def __init__(self, output_dir='habitat_maps'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def create_habitat_map(self, point_data, resolution=0.5):
        """Create continuous habitat map from point data."""
        # Extract coordinates and values
        lons = point_data['longitude'].values
        lats = point_data['latitude'].values
        values = point_data['value'].values

        # Create grid
        lon_min, lon_max = lons.min(), lons.max()
        lat_min, lat_max = lats.min(), lats.max()

        grid_lon = np.arange(lon_min, lon_max, resolution)
        grid_lat = np.arange(lat_min, lat_max, resolution)
        grid_lon, grid_lat = np.meshgrid(grid_lon, grid_lat)

        # Interpolate
        grid_values = griddata(
            (lons, lats),
            values,
            (grid_lon, grid_lat),
            method='cubic',
            fill_value=0
        )

        return grid_lon, grid_lat, grid_values

    def save_as_geotiff(self, grid_lon, grid_lat, grid_values, output_name='habitat_map'):
        """Save habitat map as GeoTIFF."""
        transform = from_origin(
            grid_lon.min(),
            grid_lat.max(),
            grid_lon[0, 1] - grid_lon[0, 0],
            grid_lat[0, 0] - grid_lat[1, 0]
        )

        with rasterio.open(
            f'{self.output_dir}/{output_name}.tif',
            'w',
            driver='GTiff',
            height=grid_values.shape[0],
            width=grid_values.shape[1],
            count=1,
            dtype=grid_values.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            dst.write(grid_values, 1)

        return f'{self.output_dir}/{output_name}.tif'
