"""
Spatial Interpolation
Interpolates point data to continuous surfaces.
"""

import numpy as np
from scipy.interpolate import griddata, Rbf
from scipy.spatial import cKDTree


class SpatialInterpolator:
    def __init__(self):
        pass

    def interpolate_cubic(self, points, values, grid_x, grid_y):
        """Cubic interpolation of point data."""
        grid_z = griddata(
            points,
            values,
            (grid_x, grid_y),
            method='cubic',
            fill_value=np.nan
        )
        return grid_z

    def interpolate_linear(self, points, values, grid_x, grid_y):
        """Linear interpolation of point data."""
        grid_z = griddata(
            points,
            values,
            (grid_x, grid_y),
            method='linear',
            fill_value=np.nan
        )
        return grid_z

    def interpolate_rbf(self, points, values, grid_x, grid_y, function='multiquadric'):
        """Radial basis function interpolation."""
        rbf = Rbf(
            points[:, 0],
            points[:, 1],
            values,
            function=function
        )
        grid_z = rbf(grid_x, grid_y)
        return grid_z

    def interpolate_idw(self, points, values, grid_x, grid_y, power=2):
        """Inverse distance weighting interpolation."""
        tree = cKDTree(points)
        grid_points = np.column_stack([grid_x.ravel(), grid_y.ravel()])

        distances, indices = tree.query(grid_points, k=5)

        weights = 1 / (distances ** power)
        weights /= weights.sum(axis=1, keepdims=True)

        interpolated = np.sum(values[indices] * weights, axis=1)
        grid_z = interpolated.reshape(grid_x.shape)

        return grid_z
