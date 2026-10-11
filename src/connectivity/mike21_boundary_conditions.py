"""
MIKE 21 Boundary Conditions
Set boundary conditions for MIKE 21 FM.
"""

import numpy as np
import pandas as pd
from pathlib import Path


class MIKE21BoundaryConditions:
    def __init__(self, output_dir='mike21_boundary'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_tidal_boundary(self, tidal_data, boundary_name='tidal'):
        """Create tidal boundary condition file."""
        output_file = self.output_dir / f'{boundary_name}.bnd'

        with open(output_file, 'w') as f:
            f.write(f"[Boundary]\n")
            f.write(f"name = {boundary_name}\n")
            f.write(f"type = Tidal\n")
            f.write(f"n_constituents = {len(tidal_data)}\n\n")

            for constituent, params in tidal_data.items():
                f.write(f"[{constituent}]\n")
                f.write(f"amplitude = {params['amplitude']}\n")
                f.write(f"phase = {params['phase']}\n")
                f.write(f"speed = {params['speed']}\n\n")

        print(f"Tidal boundary saved to {output_file}")
        return output_file

    def create_elevation_boundary(self, elevation_data, boundary_name='elevation'):
        """Create elevation boundary condition file."""
        output_file = self.output_dir / f'{boundary_name}.bnd'

        with open(output_file, 'w') as f:
            f.write(f"[Boundary]\n")
            f.write(f"name = {boundary_name}\n")
            f.write(f"type = Elevation\n")
            f.write(f"n_points = {len(elevation_data)}\n\n")

            for i, (time, elev) in enumerate(elevation_data.items()):
                f.write(f"{time} {elev}\n")

        print(f"Elevation boundary saved to {output_file}")
        return output_file

    def create_current_boundary(self, current_data, boundary_name='current'):
        """Create current boundary condition file."""
        output_file = self.output_dir / f'{boundary_name}.bnd'

        with open(output_file, 'w') as f:
            f.write(f"[Boundary]\n")
            f.write(f"name = {boundary_name}\n")
            f.write(f"type = Current\n")
            f.write(f"n_points = {len(current_data)}\n\n")

            for i, (time, (u, v)) in enumerate(current_data.items()):
                f.write(f"{time} {u} {v}\n")

        print(f"Current boundary saved to {output_file}")
        return output_file


if __name__ == "__main__":
    bc = MIKE21BoundaryConditions()

    tidal_data = {
        'M2': {'amplitude': 1.2, 'phase': 45.0, 'speed': 28.984},
        'S2': {'amplitude': 0.4, 'phase': 60.0, 'speed': 30.0},
        'K1': {'amplitude': 0.3, 'phase': 120.0, 'speed': 15.041},
        'O1': {'amplitude': 0.2, 'phase': 100.0, 'speed': 13.943},
    }

    bc.create_tidal_boundary(tidal_data)
